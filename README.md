# 🖥️ Touch Kiosk App (Python + PySide6)

This is a simple fullscreen touch kiosk application built with Python and PySide6. It is designed to run on one or two screens and automatically switches to a local video (like a cartoon) when there's no internet connection.

---

## ✅ Features

- Fullscreen web browser view
- Works with 1 or 2 screens
- Touch screen support
- Automatically plays a video (fallback.mp4) when offline
- Tries to reconnect to the internet every 30 seconds
- Runs on both Windows and Raspberry Pi 4

---

## 📁 Folder Structure

touch_kiosk/
├── assets/
│ └── fallback.mp4 # Local video for offline mode
├── kiosk/
│ └── window.py # Main window logic
├── utils/
│ └── logger.py # Logging utility
├── installer/
│ └── install_kiosk.sh # Installer for Raspberry Pi
├── config.py # Kiosk configuration (URL, settings)
├── main.py # App entry point
├── README.md # This file

yaml
Copy
Edit

---

## ⚙️ How to Use

### On Windows (for testing)

1. Install Python 3
2. Install required packages:

```bash
pip install PySide6
Add your video as assets/fallback.mp4

Run the app:

python main.py
On Raspberry Pi
Copy the entire touch_kiosk/ folder to the Pi

Run the installer:

cd touch_kiosk/installer
chmod +x install_kiosk.sh
./install_kiosk.sh
Reboot the Pi:

sudo reboot
The app will run automatically on boot.

🔁 Offline Mode
If the app can't load the webpage (e.g., no internet), it will:

Show the local video in full screen

Loop the video continuously

Check again every 30 seconds

✍️ Configuration
Change the website URL in config.py:

URLS = [
    "https://your-website.com"
]
📌 Requirements
Python 3.10+

PySide6

QtWebEngine and QtMultimedia libraries