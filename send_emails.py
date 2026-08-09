import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

# --- CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "jaiswalakshay2709@gmail.com"        # 👈 Put your Gmail here
SENDER_PASSWORD = "xezd trgq ngdh zcnv"   # 👈 Paste your 16-character App Password here (no spaces)

CSV_PATH = "students.csv"

def send_certificates():
    # Connect to Gmail Server
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
    except Exception as e:
        print(f"❌ Failed to connect or login to Gmail. Check your email or App Password. Error: {e}")
        return

    # Read CSV and send emails
    with open(CSV_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            name = row.get('name')
            email = row.get('email')
            
            # Safety Check: Skip empty lines at the bottom of the CSV
            if not name or not email:
                continue
                
            clean_name = name.strip().replace(" ", "_")
            cert_filename = f"cert_{clean_name}.png"
            
            if not os.path.exists(cert_filename):
                print(f"⚠️ Certificate file missing for {name}, skipping...")
                continue
                
            print(f"✉️ Sending email to {name.strip()} ({email.strip()})...")
            
            # Create the email structure
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = email.strip()
            msg['Subject'] = f"Google Student Ambassador Program: Pitch Night Participation Certificate - {name.strip()}"

            # Modern, clean email body
            body = f"""Hi {name.strip()},

Thank you for your incredible contribution and enthusiasm during the Pitch Night Edition! Your innovation and energy truly stood out.

Please find your official Certificate of Participation attached to this email.

Best regards,
Google Student Ambassador Program Team"""
            
            msg.attach(MIMEText(body, 'plain'))

            # Attach the certificate image
            with open(cert_filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={cert_filename}",
                )
                msg.attach(part)

            # Send it!
            try:
                server.send_message(msg)
                print(f"✅ Successfully sent to {name.strip()}!")
            except Exception as e:
                print(f"❌ Failed to send to {name.strip()}. Error: {e}")
                
    server.quit()
    print("\n🏁 Process complete! All certificates have been emailed automatically.")

if __name__ == "__main__":
    send_certificates()