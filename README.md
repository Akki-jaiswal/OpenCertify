# OpenCertify

OpenCertify is a robust, highly customizable certificate generation and dispatch portal. Design your certificate template visually via a Sandbox UI, overlay participant names, dates, and signatures, and email them out automatically in bulk!

## Features
- **Visual Sandbox**: Drag-and-drop or slider-based positioning for text elements.
- **Auto-Scaling**: Name fonts scale dynamically for long names.
- **Text & Image Signatures**: Upload a PNG signature or type one out and style it.
- **Robust CSV Parsing**: Automatically handles different delimiters (commas, semicolons) and encodings to prevent crashes.
- **Bring Your Own Email (BYOE)**: Input your own SMTP credentials directly on the UI to send emails from your own account securely.

## Local Deployment

1. **Clone the repository**
2. **Install requirements**: 
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server**:
   ```bash
   python server.py
   ```
4. **Access the portal**: Open `http://localhost:5000` in your web browser.

## Docker Deployment (Render, Heroku, VPS)

OpenCertify includes a `Dockerfile` for easy deployment on any PaaS provider like Render, Railway, or Heroku.

1. Create a new Web Service on Render/Railway and connect your GitHub repository.
2. The platform will automatically detect the `Dockerfile` and build the application.
3. Once deployed, anyone can access your public URL and use the tool by inputting their own Gmail App Password.

## Security Note

If you plan to use this privately and don't want to enter your password every time, you can create a `.env` file in the root directory:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
```

**Never commit your `.env` file to a public repository!**
