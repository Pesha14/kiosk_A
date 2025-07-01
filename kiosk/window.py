from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt
from config import KIOSK_OPTIONS

class KioskWindow(QMainWindow):
    def __init__(self, screen: QScreen, url: str, logger):
        super().__init__()

        if KIOSK_OPTIONS.get("fullscreen", True):
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowState(Qt.WindowFullScreen)

        self.setGeometry(screen.geometry())
        self.logger = logger
        self.logger.info(f"Launching kiosk on screen '{screen.name()}' with URL: {url}")

        if KIOSK_OPTIONS.get("touch_enabled", True):
            self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.browser = QWebEngineView()
        self.browser.load(url)
        self.setCentralWidget(self.browser)

        self.showFullScreen()
