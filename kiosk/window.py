from PySide6.QtWidgets import (
    QMainWindow, QWidget, QStackedLayout, QVBoxLayout,
    QPushButton, QHBoxLayout
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QScreen, QKeyEvent
from config import KIOSK_OPTIONS, DEV_MODE
import os


class KioskWindow(QMainWindow):
    def __init__(self, screen: QScreen, url: str, logger):
        super().__init__()
        self.logger = logger
        self.url = url
        
        
        if KIOSK_OPTIONS.get("fullscreen", True) and not DEV_MODE:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setWindowState(Qt.WindowFullScreen)

        self.setGeometry(screen.geometry())
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        # Main container and layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Top bar with Back button
        self.back_button = QPushButton("⬅ Back")
        self.back_button.setFixedHeight(40)
        self.back_button.setEnabled(False)
        self.back_button.clicked.connect(self.go_back)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.back_button)
        top_bar.addStretch()
        self.main_layout.addLayout(top_bar)

        # Stacked layout for browser and fallback video
        self.stack_layout = QStackedLayout()
        self.main_layout.addLayout(self.stack_layout)

        # Web browser setup
        self.browser = QWebEngineView()
        self.browser.load(QUrl(self.url))
        self.browser.loadFinished.connect(self.handle_load_result)
        self.browser.urlChanged.connect(self.update_back_button)
        self.stack_layout.addWidget(self.browser)

        # Fallback video player setup
        self.video_widget = QVideoWidget()
        self.video_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.video_player.setAudioOutput(self.audio_output)
        self.video_player.setVideoOutput(self.video_widget)

        fallback_path = os.path.abspath("assets/fallback.mp4")
        self.video_player.setSource(QUrl.fromLocalFile(fallback_path))
        self.video_player.setLoops(-1)
        self.stack_layout.addWidget(self.video_widget)

        # Show browser by default
        self.stack_layout.setCurrentWidget(self.browser)
        self.showFullScreen()

        # Setup reconnect timer (offline fallback)
        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.setInterval(5000)
        self.reconnect_timer.timeout.connect(self.retry_online)

    def handle_load_result(self, ok: bool):
        if ok:
            self.logger.info(f"Page loaded: {self.url}")
            self.stop_video_fallback()
        else:
            self.logger.warning("Failed to load page — showing fallback video.")
            self.start_video_fallback()

    def start_video_fallback(self):
        self.stack_layout.setCurrentWidget(self.video_widget)
        self.video_player.play()
        self.reconnect_timer.start()

    def stop_video_fallback(self):
        if self.stack_layout.currentWidget() == self.video_widget:
            self.video_player.stop()
            self.stack_layout.setCurrentWidget(self.browser)
        self.reconnect_timer.stop()

    def retry_online(self):
        self.logger.info("Retrying to connect...")
        self.browser.load(QUrl(self.url))

    def go_back(self):
        if self.browser.history().canGoBack():
            self.browser.back()

    def update_back_button(self, url):
        self.back_button.setEnabled(self.browser.history().canGoBack())

    def keyPressEvent(self, event: QKeyEvent):

        blocked_keys = [Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Q]
        if event.key() in blocked_keys:
            return
        

        if DEV_MODE and event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_X:
            self.logger.warning("Developer exit triggered with Ctrl+X")
            self.close()

        super().keyPressEvent(event)
