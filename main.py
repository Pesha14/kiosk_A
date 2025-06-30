# main.py
import sys
from PySide6.QtWidgets import QApplication
from config import URLS
from kiosk.window import KioskWindow


def main():
    app = QApplication(sys.argv)
    screens = app.screens()

    if len(screens) == 0:
        print("No screens detected. Please connect at least one display.")
        sys.exit(1)

    # Always create at least one window
    window1 = KioskWindow(screens[0], URLS[0])
    window1.show()

    # If a second screen exists and a second URL is configured
    if len(screens) > 1 and len(URLS) > 1:
        window2 = KioskWindow(screens[1], URLS[1])
        window2.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
