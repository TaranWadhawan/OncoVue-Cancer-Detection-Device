import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QProgressBar, QWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor


class LoaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oncovue - Loading Diagnostics")
        self.setMinimumSize(1020, 720)
        
        # Central Widget & Background Setup (Soft Pastel Gradient Base)
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setStyleSheet("""
            #CentralWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #FAF7FF, 
                    stop:0.6 #F3E8FF, 
                    stop:1 #E9D5FF);
            }
        """)
        self.setCentralWidget(self.central_widget)
        
        # Master Vertical Layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Frosted glass central loader card
        self.card_widget = QWidget()
        self.card_widget.setObjectName("LoaderCard")
        self.card_widget.setFixedSize(540, 320)
        self.card_widget.setStyleSheet("""
            #LoaderCard {
                background-color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 20px;
            }
        """)
        
        # Soft outer depth shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(109, 40, 217, 20))
        shadow.setOffset(0, 10)
        self.card_widget.setGraphicsEffect(shadow)
        
        self.main_layout.addWidget(self.card_widget)
        
        # Internal Card Layout
        self.layout = QVBoxLayout(self.card_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(25)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        # Title Label (Deep Amethyst Branding)
        self.lbl_title = QLabel("Initializing System Diagnostics")
        self.lbl_title.setStyleSheet("""
            font-family: 'Poppins', 'Inter', 'Segoe UI', sans-serif;
            color: #2E1065; /* Deep Amethyst */
            font-size: 22px; 
            font-weight: bold;
            background: transparent;
        """)
        self.layout.addWidget(self.lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Indeterminate Progress Tracker (Gradient Chunk Indicator)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(400, 12)
        self.progress_bar.setRange(0, 0) # Keep indeterminate looping state
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(109, 40, 217, 0.08); /* Frosted lavender track */
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9); /* Rose to Orchid gradient */
                border-radius: 6px;
            }
        """)
        self.layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Status Label (Velvet Slate Description Text)
        self.lbl_status = QLabel("Analysing and evaluting the Image")
        self.lbl_status.setStyleSheet("""
            font-family: 'Poppins', 'Inter', sans-serif;
            color: #4C1D95; /* Velvet Slate */
            font-size: 13px;
            background: transparent;
        """)
        self.layout.addWidget(self.lbl_status, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.start(15000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoaderWindow()
    # window.showMaximized()
    window.showFullScreen()
    sys.exit(app.exec())