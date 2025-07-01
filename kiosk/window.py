# kiosk/window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QStackedLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QScreen
from config import KIOSK_OPTIONS
import os

class KioskWindow(QMainWindow):
    def __init__(self, screen: QScreen, url: str, logger):
        super().__init__()
        self.logger = logger
        self.url = url

        if KIOSK_OPTIONS.get("fullscreen", True):
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowState(Qt.WindowFullScreen)
        self.setGeometry(screen.geometry())

        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        # Main layout (stack: browser or video)
        self.central_widget = QWidget()
        self.layout = QStackedLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Web browser
        self.browser = QWebEngineView()
        self.browser.load(QUrl(self.url))
        self.browser.loadFinished.connect(self.handle_load_result)
        self.layout.addWidget(self.browser)

        # Fallback video player
        self.video_widget = QVideoWidget()
        self.video_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_player.setAudioOutput(self.audio_output)
        self.video_player.setVideoOutput(self.video_widget)

        fallback_path = os.path.abspath("assets/fallback.mp4")
        self.video_player.setSource(QUrl.fromLocalFile(fallback_path))
        self.video_player.setLoops(-1)
        self.layout.addWidget(self.video_widget)

        self.layout.setCurrentWidget(self.browser)
        self.showFullScreen()

        # Retry if offline
        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.setInterval(30000)  # 30 seconds
        self.reconnect_timer.timeout.connect(self.retry_online)

    def handle_load_result(self, ok: bool):
        if ok:
            self.logger.info(f"✅ Page loaded: {self.url}")
            self.stop_video_fallback()
        else:
            self.logger.warning("❌ Failed to load page — showing fallback video.")
            self.start_video_fallback()

    def start_video_fallback(self):
        self.layout.setCurrentWidget(self.video_widget)
        self.video_player.play()
        self.reconnect_timer.start()

    def stop_video_fallback(self):
        if self.layout.currentWidget() == self.video_widget:
            self.video_player.stop()
            self.layout.setCurrentWidget(self.browser)
        self.reconnect_timer.stop()

    def retry_online(self):
        self.logger.info("🔁 Retrying to connect...")
        self.browser.load(QUrl(self.url))
