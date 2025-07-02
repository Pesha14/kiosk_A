# 🖥️ Touch Kiosk App (Python + PySide6)

This is a simple fullscreen touch kiosk application built with Python and PySide6. It is designed to run on one or two screens and automatically switches to a local video
 (like an ad or a cartoon) when there's no internet connection.



## ✅ Features

- Fullscreen web browser view
- Works with 1 or 2 screens (HDMI 1 and 2 on Raspberry Pi 4/5)
- Touch screen support
- Automatically plays a video (`fallback.mp4`) when offline
- Retries to reconnect every 30 seconds
- Back button for page navigation
- Developer-only exit shortcut (Ctrl+X)
- Runs on both Windows and Raspberry Pi 4 / 5


## 📁 Folder Structure

touch_kiosk/
├── assets/
│ └── fallback.mp4 # Local video for offline mode
├── kiosk/
│ └── window.py # Main window logic
├── utils/
│ └── logger.py # Logging utility
├── installer/
│ └── install_kiosk.sh # Installer script for Raspberry Pi
├── config.py # Kiosk configuration (URLs, settings)
├── main.py # App entry point
├── README.md # This file



## ⚙️ How to Use

### 🧪 On Windows (for testing)

1. **Install Python 3.10+**
2. **Install required packages**:

pip install PySide6
Add your fallback video:

Place your video at: assets/fallback.mp4
Run the app:


python main.py
🍓 On Raspberry Pi 4 / 5
Copy the entire folder to the Pi (e.g., using USB or Git):


cd installer
chmod +x install_kiosk.sh
./install_kiosk.sh
This will:

Install Python dependencies (PySide6, FFmpeg)

Set up the environment

Ensure QtMultimedia & QtWebEngine are available

Reboot the Pi:


sudo reboot
Run the app manually:


cd ~/touch_kiosk
python main.py
(Optional: You can add this command to autostart on boot via systemd or .bashrc)

🔁 Offline Mode (Fallback)
If the internet or the webpage is down:

The app shows assets/fallback.mp4 in fullscreen

Loops the video continuously

Automatically checks the connection every 30 seconds

Returns to the browser once reconnected

✍️ Configuration
Open config.py to update:

URLS = [
    "https://your-kiosk-url.com",  # Screen 1
    "https://your-second-url.com"  # Screen 2 (optional)
]

KIOSK_OPTIONS = {
    "fullscreen": True,
    "touch_enabled": True,
    "enable_logging": True
}

DEV_MODE = True  # Set to False for production (disables Ctrl+X exit)
📽️ Fallback Video Tips
Recommended video settings for best performance:

Format: .mp4 (H.264)

Resolution: 720p or 1080p

Size: under 50MB (for smoother playback)

Place it inside the assets/ folder as:


assets/fallback.mp4
📌 Requirements
Python 3.10+

PySide6

QtWebEngine + QtMultimedia libraries

FFmpeg (required for video playback)

🔐 Developer Mode (Optional)
If you're testing on Windows or want an escape key:

Set DEV_MODE = True in config.py

Press Ctrl+X to exit the app safely (only in dev mode)

👨‍💻 Author
Made with ❤️ by Pesha Enock
Feel free to contribute or fork this project!
