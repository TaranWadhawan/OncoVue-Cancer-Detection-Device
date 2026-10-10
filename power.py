import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class PowerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Power Options")
        self.setFixedSize(1280, 720)
        
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
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Top Navigation Bar Layout
        self.top_bar = QHBoxLayout()
        self.btn_back = QPushButton("← Back")
        self.btn_back.setFixedSize(110, 38)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: rgba(109, 40, 217, 0.08);
                border: 1px solid rgba(109, 40, 217, 0.18);
                color: #4C1D95; /* Velvet Slate */
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(109, 40, 217, 0.15);
                border-color: rgba(109, 40, 217, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(109, 40, 217, 0.25);
            }
        """)
        self.btn_back.clicked.connect(self.back_to_dashboard)
        self.top_bar.addWidget(self.btn_back)
        self.top_bar.addStretch()
        self.main_layout.addLayout(self.top_bar)
        
        self.main_layout.addStretch()
        
        # Central Control Panel Card
        self.card_widget = QWidget()
        self.card_widget.setObjectName("CardWidget")
        self.card_widget.setFixedSize(500, 380)
        self.card_widget.setStyleSheet("""
            #CardWidget {
                background-color: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 20px;
            }
        """)
        
        # Soft Outer Shadow for Depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(109, 40, 217, 25))  # Soft Purple glow
        shadow.setOffset(0, 10)
        self.card_widget.setGraphicsEffect(shadow)
        
        self.main_layout.addWidget(self.card_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Internal Content Layout
        self.card_layout = QVBoxLayout(self.card_widget)
        self.card_layout.setContentsMargins(40, 45, 40, 45)
        self.card_layout.setSpacing(20)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Card Section Title
        self.title_label = QLabel("System Power Options")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Cormorant Garamond', 'Georgia', serif;
            font-size: 28px;
            font-weight: 500;
            color: #2E1065; /* Deep Amethyst */
            background: transparent;
            margin-bottom: 5px;
        """)
        self.card_layout.addWidget(self.title_label)
        
        # --- Reboot System Button (Warning Warm Peach/Rose Gradient state) ---
        self.btn_reboot = QPushButton("Reboot System")
        self.btn_reboot.setFixedHeight(55)
        self.btn_reboot.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F59E0B, 
                    stop:1 #EC4899); /* Warm Peach to Rose gradient */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #FBBF24, 
                    stop:1 #F472B6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #D97706, 
                    stop:1 #DB2777);
            }
        """)
        self.btn_reboot.clicked.connect(self.trigger_reboot)
        self.card_layout.addWidget(self.btn_reboot)
        
        # --- Shutdown System Button (Critical Soft Crimson State) ---
        self.btn_shutdown = QPushButton("Shutdown System")
        self.btn_shutdown.setFixedHeight(55)
        self.btn_shutdown.setStyleSheet("""
            QPushButton {
                background-color: #EF4444; /* Soft Crimson */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:pressed {
                background-color: #B91C1C;
            }
        """)
        self.btn_shutdown.clicked.connect(self.trigger_shutdown)
        self.card_layout.addWidget(self.btn_shutdown)
        
        self.main_layout.addStretch()

    def back_to_dashboard(self):
                # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "page3.py"])
        self.close()

    def terminate_other_processes(self):
        try:
            import psutil
            current_pid = os.getpid()
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmd = proc.info['cmdline']
                    if cmd and any("python" in str(arg).lower() for arg in cmd):
                        if any(script in str(cmd) for script in ["main.py", "page1.py", "page2.py", "page3.py", "manage_admin.py", "manage_admin_page2.py", "export_page1.py"]):
                            if proc.info['pid'] != current_pid:
                                proc.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except ImportError:
            if sys.platform.startswith("win32"):
                os.system("taskkill /IM python.exe /F")
            else:
                os.system("pkill -f python")

    def trigger_reboot(self):
        self.terminate_other_processes()
        QApplication.quit()
        if sys.platform.startswith("win32"):
            os.system("shutdown /r /t 1")
        else:
            os.system("sudo reboot")
        print("reboot")

    def trigger_shutdown(self):
        self.terminate_other_processes()
        QApplication.quit()
        if sys.platform.startswith("win32"):
            os.system("shutdown /s /t 1")
        else:
            os.system("sudo poweroff")
        print("shut down")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PowerWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())