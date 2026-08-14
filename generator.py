import os
import csv
import smtplib
from PIL import Image, ImageDraw, ImageFont
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

# --- CONFIGURATION DEFAULTS ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FONT_FILE = "Poppins-SemiBoldItalic.ttf"
FONT_FILE = "Poppins-SemiBoldItalic.ttf"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def process_certificates(csv_path, template_path, signature_path, config, progress_callback=None):
    """
    Generate certificates and send emails based on the provided configuration.
    """
    try:
        # Load fonts
        try:
            name_size = max(1, int(config.get('nameFontSize', 38)))
            date_size = max(1, int(config.get('dateFontSize', 24)))
            name_font = ImageFont.truetype(FONT_FILE, size=name_size)
            date_font = ImageFont.truetype(FONT_FILE, size=date_size)
        except Exception:
            name_font = ImageFont.load_default()
            date_font = ImageFont.load_default()

        name_color = hex_to_rgb(config.get('nameColor', '#282828'))
        date_color = hex_to_rgb(config.get('dateColor', '#282828'))
        
        name_x = int(config.get('nameX', 620))
        name_y = int(config.get('nameY', 435))
        
        date_text = config.get('dateText', '')
        date_x = int(config.get('dateX', 200))
        date_y = int(config.get('dateY', 800))
        
        sig_x = int(config.get('sigX', 800))
        sig_y = int(config.get('sigY', 800))
        sig_scale = float(config.get('sigScale', 1.0))
        
        # Connect to SMTP (Strictly use user-provided credentials for security)
        sender_email = config.get('smtpEmail')
        sender_password = config.get('smtpPassword')
        
        if not sender_email or not sender_password:
            return {"status": "error", "message": "SMTP credentials (Email and App Password) are missing!"}
            
        if progress_callback: progress_callback("Connecting to SMTP Server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Process CSV robustly
        def get_rows():
            content = ""
            for enc in ['utf-8-sig', 'utf-16', 'cp1252']:
                try:
                    with open(csv_path, 'r', encoding=enc) as f:
                        test_content = f.read()
                        if '\x00' not in test_content:
                            content = test_content
                            break
                except Exception:
                    continue
            
            if not content:
                with open(csv_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                    content = f.read().replace('\x00', '')
            
            delimiter = ';' if (';' in content and content.count(';') > content.count(',')) else ','
            return list(csv.DictReader(content.splitlines(), delimiter=delimiter))
                
        rows = get_rows()
        total = len(rows)
            
        processed_count = 0
        for index, row in enumerate(rows):
                # Try to get name and email case-insensitively
                name_key = next((k for k in row.keys() if k and k.strip().lower() == 'name'), 'name')
                email_key = next((k for k in row.keys() if k and k.strip().lower() == 'email'), 'email')
                
                name = row.get(name_key)
                email = row.get(email_key)
                
                if not name or not email:
                    continue
                    
                processed_count += 1
                if progress_callback: progress_callback(f"Processing ({processed_count}/{total}): {name}...")
                
                # --- GENERATION ---
                image = Image.open(template_path).convert("RGBA")
                draw = ImageDraw.Draw(image)
                
                # Draw Name (Centered at Name X)
                text_width = draw.textlength(name, font=name_font)
                actual_name_x = name_x - (text_width / 2)
                draw.text((actual_name_x, name_y), name, fill=name_color, font=name_font)
                
                # Draw Date
                if date_text:
                    draw.text((date_x, date_y), date_text, fill=date_color, font=date_font)
                
                # Add Signature
                sig_text = config.get('sigText', '').strip()
                if sig_text:
                    try:
                        sig_size = max(1, int(config.get('sigFontSize', 40)))
                        sig_font = ImageFont.truetype(FONT_FILE, size=sig_size)
                    except Exception:
                        sig_font = ImageFont.load_default()
                    sig_color = hex_to_rgb(config.get('sigColor', '#282828'))
                    draw.text((sig_x, sig_y), sig_text, fill=sig_color, font=sig_font)
                elif signature_path and os.path.exists(signature_path):
                    sig_img = Image.open(signature_path).convert("RGBA")
                    new_size = (int(sig_img.width * sig_scale), int(sig_img.height * sig_scale))
                    sig_img = sig_img.resize(new_size, Image.Resampling.LANCZOS)
                    image.paste(sig_img, (sig_x, sig_y), sig_img)
                
                # Save certificate
                clean_name = name.strip().replace(" ", "_")
                cert_filename = f"cert_{clean_name}.png"
                # Convert back to RGB to save as PNG properly if it has no alpha or just save as PNG
                image.save(cert_filename, "PNG")
                
                # --- EMAILING ---
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email.strip()
                
                raw_subject = config.get('emailSubject', 'Certificate of Participation')
                raw_body = config.get('emailBody', 'Please find your certificate attached.')
                
                msg['Subject'] = raw_subject.replace('{name}', name.strip())
                body = raw_body.replace('{name}', name.strip())
               
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                with open(cert_filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={cert_filename}")
                    msg.attach(part)

                server.send_message(msg)
                
                # Increment the global stats counter
                import stats_manager
                stats_manager.increment()
                
                # Clean up generated file
                os.remove(cert_filename)
                
        server.quit()
        if processed_count == 0:
            if progress_callback: progress_callback("⚠️ WARNING: No valid names/emails found in the CSV. Make sure your column headers are 'name' and 'email'.")
            return {"status": "error", "message": "No valid rows found in CSV."}
            
        if progress_callback: progress_callback(f"✅ Process complete! {processed_count} certificates emailed.")
        return {"status": "success", "message": "All certificates sent successfully!"}
        
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        with open("debug.log", "w", encoding="utf-8") as f:
            f.write(trace)
        if progress_callback: progress_callback(f"❌ Error:\n{trace}")
        return {"status": "error", "message": str(e)}
