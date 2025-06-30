# kiosk/window.py
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen


class KioskWindow(QMainWindow):
    def __init__(self, screen: QScreen, url: str):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setGeometry(screen.geometry())
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        browser = QWebEngineView()
        browser.load(url)
        self.setCentralWidget(browser)

        self.showFullScreen()
