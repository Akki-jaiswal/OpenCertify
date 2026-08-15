<div align="center">
  <img src="static/logo.jpg" alt="OpenCertify Logo" width="150"/>
  <h1>🎓 OpenCertify</h1>
  <p><b>A well designed, open-source certificate generation and dispatch portal.</b></p>
</div>

<br/>

OpenCertify is an advanced, user-friendly tool built for event organizers, educators, and community leaders. It allows you to visually design certificates, automatically overlay participant names from a CSV, and instantly dispatch hundreds of emails directly from your own Gmail account.

## ✨ Features

- **🎨 Visual Sandbox:** Drag-and-drop or slider-based positioning for text elements directly on your template.
- **📱 Glassmorphism UI:** A stunning, modern, and highly responsive user interface.
- **🚀 Bring Your Own Email (BYOE):** No central server required. Input your own Gmail App Password directly on the UI to securely send emails from your own account.
- **✍️ Dynamic Signatures:** Upload a PNG signature or type one out and style it digitally.
- **📊 Live Terminal & Stats:** Watch the real-time progress of your emails being sent via Server-Sent Events (SSE).
- **🛡️ Secure & Local:** Runs 100% locally on your machine, ensuring complete privacy for your participants' data.

---

## 🚀 Quick Start (Local Setup)

Because modern cloud providers (like Render or Heroku) strictly block outgoing email ports on their free tiers to prevent spam, **OpenCertify is designed to be run locally on your own computer.**

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Akki-jaiswal/OpenCertify.git
   cd OpenCertify
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python server.py
   ```

4. **Access the portal:**
   Open your browser and navigate to `http://localhost:5000`



---

## 📝 Usage Guide

1. **Prepare your CSV:** Create a CSV file with at least two columns: `Name` and `Email`.
2. **Prepare your Template:** Ensure you have a blank certificate template (JPG/PNG).
3. **App Password:** You must use a **Google App Password** (not your regular Gmail password). 
   - Go to Google Account > Security > 2-Step Verification > App Passwords.
   - Generate a new password and paste it into OpenCertify.
4. **Design & Send:** Use the sliders to position the text, and click **Generate & Send Emails**!

## 🤝 Contributing

Contributions are always welcome! Whether it's a bug fix, new feature, or documentation improvement, please feel free to open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
