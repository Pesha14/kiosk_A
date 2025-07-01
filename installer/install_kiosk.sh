
#cd ~/touch_kiosk/installer
#chmod +x install_kiosk.sh


echo "🧩 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Installing Python and PySide6..."
sudo apt install python3 python3-pip libqt6webengine6 -y
pip3 install PySide6

echo "📁 Copying Kiosk App to ~/touch_kiosk ..."
mkdir -p ~/touch_kiosk

# Copy only if not already in ~/touch_kiosk
if [[ "$PWD" != "/home/pi/touch_kiosk" ]]; then
  cp -r ../* ~/touch_kiosk/
fi

echo "🛠 Creating systemd service..."
cat <<EOF | sudo tee /etc/systemd/system/kiosk.service
[Unit]
Description=Touch Kiosk App
After=graphical.target

[Service]
User=pi
Environment=DISPLAY=:0
ExecStart=/usr/bin/python3 /home/pi/touch_kiosk/main.py
Restart=always

[Install]
WantedBy=graphical.target
EOF

echo "🔁 Reloading and enabling kiosk service..."
sudo systemctl daemon-reload
sudo systemctl enable kiosk.service

echo "✅ Installation complete!"
echo "⚠️ The kiosk app will start automatically on next reboot."
echo "💡 Reboot now with: sudo reboot"
