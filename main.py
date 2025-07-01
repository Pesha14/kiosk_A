import sys
from PySide6.QtWidgets import QApplication
from config import URLS
from kiosk.window import KioskWindow
from utils.logger import setup_logger

def main():
    app = QApplication(sys.argv)
    logger = setup_logger()

    screens = app.screens()
    logger.info(f"Detected {len(screens)} screen(s).")

    if len(screens) == 0:
        logger.error("No screens detected.")
        sys.exit(1)

    # Load at least one window
    window1 = KioskWindow(screens[0], URLS[0], logger)
    window1.show()

    # Load second window only if screen and URL are available
    if len(screens) > 1 and len(URLS) > 1:
        window2 = KioskWindow(screens[1], URLS[1], logger)
        window2.show()
    else:
        logger.warning("Only one screen or URL provided. Skipping second window.")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
