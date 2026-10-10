import sys
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QGridLayout, QPushButton, QWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QDateTime, QTimer

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Dashboard")
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
        
        # Main Layout Alignment
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Glassmorphic Main Menu Card
        self.menu_card = QWidget()
        self.menu_card.setObjectName("MenuCard")
        self.menu_card.setFixedSize(580, 520)
        self.menu_card.setStyleSheet("""
            #MenuCard {
                background-color: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 24px;
            }
        """)
        
        # Soft Outer Shadow for Depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(109, 40, 217, 25))  # Muted purple ambient shadow
        shadow.setOffset(0, 12)
        self.menu_card.setGraphicsEffect(shadow)
        
        self.main_layout.addWidget(self.menu_card)
        
        # Grid Layout Setup for clean 2-column distribution
        self.card_layout = QGridLayout(self.menu_card)
        self.card_layout.setContentsMargins(40, 45, 40, 45)
        self.card_layout.setHorizontalSpacing(15)
        self.card_layout.setVerticalSpacing(15)
        
        # Section Header Branding
        self.title_label = QLabel("Dashboard")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Cormorant Garamond', 'Georgia', serif;
            font-size: 36px;
            font:bold;
            font-weight: 500;
            color: #2E1065; /* Deep Amethyst */
            background: transparent;
            margin-bottom: 5px;
        """)
        self.card_layout.addWidget(self.title_label, 0, 0, 1, 2)
        
        # --- Primary Action Buttons (Gradient Accent and Solid Orchid) ---
        self.btn_analysis = QPushButton("Analysis")
        self.btn_analysis.setMinimumHeight(52)
        self.btn_analysis.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EC4899, stop:1 #6D28D9);
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F472B6, stop:1 #7C3AED);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #DB2777, stop:1 #5B21B6);
            }
        """)
        self.btn_analysis.clicked.connect(self.open_analysis)
        self.card_layout.addWidget(self.btn_analysis, 1, 0)
        
        self.btn_report = QPushButton("View Report and data")
        self.btn_report.setMinimumHeight(52)
        self.btn_report.setStyleSheet("""
            QPushButton {
                background-color: #6D28D9; /* Solid Orchid Purple */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
        """)
        self.btn_report.clicked.connect(self.open_report)
        self.card_layout.addWidget(self.btn_report, 1, 1)
        
        # --- Secondary Data Buttons (Translucent Lavender styles) ---
        self.btn_export = QPushButton("Export Data")
        self.btn_export.setMinimumHeight(52)
        self.btn_export.setStyleSheet("""
            QPushButton {
                background-color: rgba(109, 40, 217, 0.08);
                border: 1px solid rgba(109, 40, 217, 0.2);
                color: #4C1D95; /* Velvet Slate */
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(109, 40, 217, 0.15);
                border-color: rgba(109, 40, 217, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(109, 40, 217, 0.25);
            }
        """)
        self.btn_export.clicked.connect(self.open_export)
        self.card_layout.addWidget(self.btn_export, 2, 0)
        
        self.btn_manage = QPushButton("Manage admin user")
        self.btn_manage.setMinimumHeight(52)
        self.btn_manage.setStyleSheet("""
            QPushButton {
                background-color: rgba(109, 40, 217, 0.08);
                border: 1px solid rgba(109, 40, 217, 0.2);
                color: #4C1D95;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(109, 40, 217, 0.15);
                border-color: rgba(109, 40, 217, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(109, 40, 217, 0.25);
            }
        """)
        self.btn_manage.clicked.connect(self.open_manage)
        self.card_layout.addWidget(self.btn_manage, 2, 1)

        # --- Utility Actions (Soft Muted Palette) ---
        self.btn_sync = QPushButton("Sync Data")
        self.btn_sync.setMinimumHeight(52)
        self.btn_sync.setStyleSheet("""
            QPushButton {
                background-color: rgba(192, 132, 252, 0.12);
                border: 1px solid rgba(192, 132, 252, 0.25);
                color: #2E1065;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(192, 132, 252, 0.2);
                border-color: rgba(192, 132, 252, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(192, 132, 252, 0.3);
            }
        """)
        self.btn_sync.clicked.connect(self.sync)
        self.card_layout.addWidget(self.btn_sync, 3, 0)
        
        self.btn_exit = QPushButton("Exit System")
        self.btn_exit.setMinimumHeight(52)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: rgba(76, 29, 149, 0.08);
                border: 1px solid rgba(76, 29, 149, 0.15);
                color: #4C1D95;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(76, 29, 149, 0.15);
                border-color: rgba(76, 29, 149, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(76, 29, 149, 0.25);
            }
        """)
        self.btn_exit.clicked.connect(self.exit_app)
        self.card_layout.addWidget(self.btn_exit, 3, 1)

        # --- System Power Control (Full-width Accent at Bottom) ---
        self.btn_power = QPushButton("System Power Options")
        self.btn_power.setMinimumHeight(52)
        self.btn_power.setStyleSheet("""
            QPushButton {
                background-color: #EF4444; /* Soft Crimson */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
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
        self.btn_power.clicked.connect(self.power)
        self.card_layout.addWidget(self.btn_power, 4, 0, 1, 2)

        self.lbl_datetime = QLabel()
        self.lbl_datetime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_datetime.setStyleSheet("""
            font-family: 'Poppins', 'Inter', sans-serif;
            font-size: 14px;
            font-weight: bold;
            color: #6D28D9;
            background: transparent;
            margin-bottom: 10px;
        """)
        self.card_layout.addWidget(self.lbl_datetime)
        
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_datetime_display)
        self.time_timer.start(1000)
        self.update_datetime_display()

    def open_analysis(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "analysis_page1.py"])
        self.close()

    def open_report(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "report_page1.py"])
        self.close()

    def open_export(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "export_page1.py"])
        self.close()

    def open_manage(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])        
        subprocess.Popen([sys.executable, "manage_admin_page1.py"])
        self.close()

    def exit_app(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])        
        subprocess.Popen([sys.executable, "exit.py"])
        self.close()

    def power(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])        
        subprocess.Popen([sys.executable, "power.py"])
        self.close()

    def sync(self):
        # self.timer.stop()
        subprocess.Popen([sys.executable, "loader_larger.py"])        
        subprocess.Popen([sys.executable, "sync.py"])
        self.close()

    def update_datetime_display(self):
        current_dt = QDateTime.currentDateTime().toString("dd-MM-yyyy   hh:mm:ss AP")
        self.lbl_datetime.setText(current_dt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())