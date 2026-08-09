import csv
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "template.png"
CSV_PATH = "students.csv"

FONT_FILE = "Poppins-SemiBoldItalic.ttf" 

def generate_certificates():
    try:
        font = ImageFont.truetype(FONT_FILE, size=38) # Slightly larger size
    except IOError:
        print(f"Could not find {FONT_FILE}. Using default font.")
        font = ImageFont.load_default()

    with open(CSV_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            name = row['name']
            print(f"Generating certificate for: {name}")
            
            image = Image.open(TEMPLATE_PATH)
            draw = ImageDraw.Draw(image)
            
            # Center X is 620 (1240 / 2)
            text_width = draw.textlength(name, font=font)
            x_position = 620 - (text_width / 2)
            
            y_position = 435  # Moves text further down

            # 4. Draw the text onto the image
            text_color = (40, 40, 40)
            draw.text((x_position, y_position), name, fill=text_color, font=font)
            
            # 5. Save the personalized certificate
            clean_name = name.replace(" ", "_")
            image.save(f"cert_{clean_name}.png")

if __name__ == "__main__":
    generate_certificates()
    print("✨ All certificates generated successfully with the new font!")