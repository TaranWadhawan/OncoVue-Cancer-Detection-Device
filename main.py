import sys
import os
# import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel, QWidget, QGraphicsDropShadowEffect
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QColor, QFont

class SplashWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Initializing")
        self.setFixedSize(1280, 720)
        
        # Remove standard OS window frame for a premium seamless look
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main container with premium soft-pastel linear gradient background
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setStyleSheet("""
            #CentralWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #FAF7FF, 
                    stop:0.5 #F9A8D4, 
                    stop:1 #C084FC);
                border-radius: 24px;
            }
        """)
        self.setCentralWidget(self.central_widget)
        
        # Master Layout
        self.master_layout = QVBoxLayout(self.central_widget)
        self.master_layout.setContentsMargins(40, 40, 40, 40)
        self.master_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Glassmorphic Content Card
        self.glass_card = QWidget()
        self.glass_card.setObjectName("GlassCard")
        self.glass_card.setStyleSheet("""
            #GlassCard {
                background-color: rgba(250, 247, 255, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.5);
                border-radius: 20px;
            }
        """)
        
        # Add soft bloom drop-shadow to the glass container
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(109, 40, 217, 40)) # Light Orchid Glow
        shadow.setOffset(0, 10)
        self.glass_card.setGraphicsEffect(shadow)
        
        self.card_layout = QVBoxLayout(self.glass_card)
        self.card_layout.setContentsMargins(20, 30, 20, 30)
        self.card_layout.setSpacing(25)
        
        # Header / Branding Layout
        self.brand_layout = QVBoxLayout()
        self.brand_layout.setSpacing(5)
        
        # Logo Text / Title (Feminine Biotech & Luxury Serif Feel)
        self.title_label = QLabel("OncoVue")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Cormorant Garamond', 'Playfair Display', 'Georgia', serif;
            font-size: 34px;
            font-weight: bold;
            font-style: italic;
            color: #6D28D9; /* Orchid Purple */
            letter-spacing: 2px;
        """)
        self.brand_layout.addWidget(self.title_label)
        
        # Tagline / Subtitle (Clean Premium Sans-Serif)
        self.tagline_label = QLabel("“We Care To Cure”")
        self.tagline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tagline_label.setStyleSheet("""
            font-family: 'Poppins', 'Inter', 'Segoe UI', sans-serif;
            font-size: 14px;
            font-weight: 500;
            color: #EC4899; /* Rose Pink */
            letter-spacing: 6px;
            text-transform: uppercase;
        """)
        self.brand_layout.addWidget(self.tagline_label)
        self.card_layout.addLayout(self.brand_layout)
        
        # Splash Image Label Container (Checks for the assets directory cleanly)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        splash_path = os.path.join("assets", "splash.png")
        if os.path.exists(splash_path):
            pixmap = QPixmap(splash_path).scaled(1200, 460, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setStyleSheet("border-radius: 12px;")
        else:
            # Fallback style matching the soft futuristic theme if splash graphic is missing
            self.image_label.setText("PREMIUM MEDICAL AI PLATFORM")
            self.image_label.setStyleSheet("""
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 16px;
                font-weight: 600;
                color: #2E1065;
                letter-spacing: 4px;
                background-color: rgba(236, 72, 153, 0.08);
                border-radius: 12px;
                border: 1px dashed rgba(109, 40, 217, 0.2);
            """)
            self.image_label.setFixedHeight(240)
            
        self.card_layout.addWidget(self.image_label)
        
        # Loading Status Info Label
        self.status_label = QLabel("Initializing Neural Networks...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-family: 'Poppins', 'Inter', sans-serif;
            font-size: 12px;
            color: #4C1D95; /* Velvet Slate Secondary Text */
            font-weight: 500;
        """)
        self.card_layout.addWidget(self.status_label)
        
        # Elegant Thin Progress Bar Container
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # Clean aesthetic (removed text from bar track)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(109, 40, 217, 0.1); /* Very light orchid tint */
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9); /* Rose to Orchid gradient */
                border-radius: 4px;
            }
        """)
        self.card_layout.addWidget(self.progress_bar)
        
        self.master_layout.addWidget(self.glass_card)
        
        # Operational Timer Logic (Unchanged behavior)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(30)
        
    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        
        # Dynamic text updates for visual immersion
        if self.progress_value == 25:
            self.status_label.setText("Securing Cloud Sync...")
        elif self.progress_value == 55:
            self.status_label.setText("Calibrating Diagnostic Parameters...")
        elif self.progress_value == 80:
            self.status_label.setText("Building Medical Workspace...")
            
        if self.progress_value >= 100:
            self.timer.stop()
            self.open_page1()
            
    def open_page1(self):
        self.timer.stop()
        # if self.cap.isOpened():
        #     self.cap.release()
            
        # Launch the fast loader first to cover the screen
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "page1.py"])
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())