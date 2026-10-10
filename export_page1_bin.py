# # # import sys
# # # # import os
# # # import os
# # # os.environ["QT_QPA_PLATFORM"] = "xcb"
# # # import re
# # # import socket
# # # import smtplib
# # # import subprocess
# # # import openpyxl
# # # from email.mime.multipart import MIMEMultipart
# # # from email.mime.text import MIMEText
# # # from email.mime.base import MIMEBase
# # # from email import encoders
# # # from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
# # #                              QHBoxLayout, QWidget, QLineEdit, QPushButton, 
# # #                              QComboBox, QScrollArea, QTextBrowser, QRadioButton, QButtonGroup, QGraphicsDropShadowEffect)
# # # from PyQt6.QtCore import Qt
# # # from PyQt6.QtGui import QPixmap, QColor
# # # from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
# # # from keyboard import VirtualKeyboard

# # # import socket
# # # orig_getaddrinfo = socket.getaddrinfo
# # # def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
# # #     if host == "smtp.gmail.com":
# # #         family = socket.AF_INET
# # #     return orig_getaddrinfo(host, port, family, type, proto, flags)
# # # socket.getaddrinfo = patched_getaddrinfo


# # # class ExportPage(QMainWindow):
# # #     def __init__(self):
# # #         super().__init__()
# # #         self.setWindowTitle("OncoVue - Export Patient Data")
# # #         self.setFixedSize(1280, 720)
        
# # #         self.data_file = r"data/data.xlsx"
# # #         self.user_file = r"data/user.xlsx"
# # #         self.selected_patient = None
        
# # #         # Central Widget & Background Setup (Soft Pastel Gradient Base)
# # #         self.central_widget = QWidget()
# # #         self.central_widget.setObjectName("CentralWidget")
# # #         self.central_widget.setStyleSheet("""
# # #             #CentralWidget {
# # #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
# # #                     stop:0 #FAF7FF, 
# # #                     stop:0.6 #F3E8FF, 
# # #                     stop:1 #E9D5FF);
# # #             }
# # #         """)
# # #         self.setCentralWidget(self.central_widget)
        
# # #         # Master Vertical Layout
# # #         self.main_layout = QVBoxLayout(self.central_widget)
# # #         self.main_layout.setContentsMargins(25, 20, 25, 20)
# # #         self.main_layout.setSpacing(15)
        
# # #         # Top Navigation Bar Layout (Glass Back Button)
# # #         self.top_bar = QHBoxLayout()
# # #         self.btn_back = QPushButton("← Back")
# # #         self.btn_back.setFixedSize(110, 38)
# # #         self.btn_back.setStyleSheet("""
# # #             QPushButton {
# # #                 background-color: rgba(109, 40, 217, 0.08);
# # #                 border: 1px solid rgba(109, 40, 217, 0.18);
# # #                 color: #4C1D95; /* Velvet Slate */
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-weight: bold;
# # #                 border-radius: 8px;
# # #                 font-size: 13px;
# # #             }
# # #             QPushButton:hover {
# # #                 background-color: rgba(109, 40, 217, 0.15);
# # #                 border-color: rgba(109, 40, 217, 0.3);
# # #             }
# # #             QPushButton:pressed {
# # #                 background-color: rgba(109, 40, 217, 0.25);
# # #             }
# # #         """)
# # #         self.btn_back.clicked.connect(self.back_to_dashboard)
# # #         self.top_bar.addWidget(self.btn_back)
# # #         self.top_bar.addStretch()
# # #         self.main_layout.addLayout(self.top_bar)
        
# # #         # Split workspace layouts
# # #         self.content_layout = QHBoxLayout()
# # #         self.main_layout.addLayout(self.content_layout)
        
# # #         # Left Panel (Frosted Glass Container for inputs)
# # #         self.left_panel = QWidget()
# # #         self.left_panel.setObjectName("LeftPanel")
# # #         self.left_panel.setFixedWidth(390)
# # #         self.left_panel.setStyleSheet("""
# # #             #LeftPanel {
# # #                 background-color: rgba(255, 255, 255, 0.72);
# # #                 border: 1px solid rgba(109, 40, 217, 0.15);
# # #                 border-radius: 16px;
# # #             }
# # #         """)
        
# # #         # Left Panel Shadow
# # #         shadow_left = QGraphicsDropShadowEffect(self)
# # #         shadow_left.setBlurRadius(25)
# # #         shadow_left.setColor(QColor(109, 40, 217, 15))
# # #         shadow_left.setOffset(0, 8)
# # #         self.left_panel.setGraphicsEffect(shadow_left)
        
# # #         self.left_layout = QVBoxLayout(self.left_panel)
# # #         self.left_layout.setSpacing(12)
# # #         self.left_layout.setContentsMargins(25, 25, 25, 25)
# # #         self.content_layout.addWidget(self.left_panel)
        
# # #         # Right Panel (Frosted Glass Container for data view)
# # #         self.right_panel = QWidget()
# # #         self.right_panel.setObjectName("RightPanel")
# # #         self.right_panel.setStyleSheet("""
# # #             #RightPanel {
# # #                 background-color: rgba(255, 255, 255, 0.72);
# # #                 border: 1px solid rgba(109, 40, 217, 0.15);
# # #                 border-radius: 16px;
# # #             }
# # #         """)
        
# # #         # Right Panel Shadow
# # #         shadow_right = QGraphicsDropShadowEffect(self)
# # #         shadow_right.setBlurRadius(25)
# # #         shadow_right.setColor(QColor(109, 40, 217, 15))
# # #         shadow_right.setOffset(0, 8)
# # #         self.right_panel.setGraphicsEffect(shadow_right)
        
# # #         self.right_layout = QVBoxLayout(self.right_panel)
# # #         self.right_layout.setContentsMargins(15, 15, 15, 15)
# # #         self.content_layout.addWidget(self.right_panel)
        
# # #         self.setup_left_panel()
# # #         self.setup_right_panel()
# # #         self.keyboard = VirtualKeyboard(self)
# # #         self.keyboard.show()
# # #         self.keyboard.move(100, 480)

# # #     def back_to_dashboard(self):
# # #                 # self.timer.stop()
# # #         subprocess.Popen([sys.executable, "loader.py"])
# # #         subprocess.Popen([sys.executable, "page3.py"])
# # #         self.close()

# # #     def get_doctors_list(self):
# # #         doctors = ["Select Doctor"]
# # #         if os.path.exists(self.user_file):
# # #             try:
# # #                 wb = openpyxl.load_workbook(self.user_file, data_only=True)
# # #                 sheet = wb.active
# # #                 for row in sheet.iter_rows(min_row=2, values_only=True):
# # #                     if len(row) >= 2 and row[1]:
# # #                         doc_name = str(row[1]).strip()
# # #                         if doc_name not in doctors:
# # #                             doctors.append(doc_name)
# # #                 wb.close()
# # #             except Exception:
# # #                 pass
# # #         return doctors

# # #     def setup_left_panel(self):
# # #         # Section Header Label
# # #         lbl_search_title = QLabel("SEARCH PATIENT DATA")
# # #         lbl_search_title.setStyleSheet("""
# # #             font-family: 'Poppins', 'Inter', sans-serif;
# # #             font-size: 11px;
# # #             font-weight: bold;
# # #             color: #6D28D9; /* Orchid Purple */
# # #             letter-spacing: 2px;
# # #             background: transparent;
# # #         """)
# # #         self.left_layout.addWidget(lbl_search_title)
        
# # #         self.s_name = QLineEdit()
# # #         self.s_name.setPlaceholderText("Patient Name")
        
# # #         self.s_gender = QComboBox()
# # #         self.s_gender.addItems(["Select Gender", "Female"])
        
# # #         self.s_age = QLineEdit()
# # #         self.s_age.setPlaceholderText("Age")
        
# # #         self.s_doctor = QComboBox()
# # #         self.s_doctor.addItems(self.get_doctors_list())
        
# # #         input_style = """
# # #             QLineEdit, QComboBox {
# # #                 border: 1px solid rgba(109, 40, 217, 0.18);
# # #                 border-radius: 6px;
# # #                 padding: 8px 12px;
# # #                 background-color: rgba(255, 255, 255, 0.9);
# # #                 color: #2E1065; /* Deep Amethyst */
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-size: 13px;
# # #             }
# # #             QLineEdit:focus, QComboBox:focus {
# # #                 border: 1.5px solid #6D28D9;
# # #                 background-color: #ffffff;
# # #             }
# # #         """
# # #         self.s_name.setStyleSheet(input_style)
# # #         self.s_gender.setStyleSheet(input_style)
# # #         self.s_age.setStyleSheet(input_style)
# # #         self.s_doctor.setStyleSheet(input_style)
        
# # #         self.left_layout.addWidget(self.s_name)
# # #         self.left_layout.addWidget(self.s_gender)
# # #         self.left_layout.addWidget(self.s_age)
# # #         self.left_layout.addWidget(self.s_doctor)
        
# # #         self.btn_search = QPushButton("Search Patient")
# # #         self.btn_search.setMinimumHeight(38)
# # #         self.btn_search.setStyleSheet("""
# # #             QPushButton {
# # #                 background-color: #6D28D9; /* Solid Orchid Purple */
# # #                 color: white;
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-weight: bold;
# # #                 border: none;
# # #                 border-radius: 6px;
# # #                 font-size: 13px;
# # #             }
# # #             QPushButton:hover {
# # #                 background-color: #7C3AED;
# # #             }
# # #         """)
# # #         self.btn_search.clicked.connect(self.search_patient)
# # #         self.left_layout.addWidget(self.btn_search)
        
# # #         # Export Option Section Header
# # #         lbl_export_title = QLabel("EXPORT OPTIONS")
# # #         lbl_export_title.setStyleSheet("""
# # #             font-family: 'Poppins', 'Inter', sans-serif;
# # #             font-size: 11px;
# # #             font-weight: bold;
# # #             color: #6D28D9;
# # #             letter-spacing: 2px;
# # #             background: transparent;
# # #             margin-top: 10px;
# # #         """)
# # #         self.left_layout.addWidget(lbl_export_title)
        
# # #         self.export_group = QButtonGroup(self)
        
# # #         self.rad_email = QRadioButton("Export via Email")
# # #         self.rad_bluetooth = QRadioButton("Export via Bluetooth")
# # #         self.rad_print = QRadioButton("Print to Printer (USB / Wi-Fi)")
# # #         self.rad_email.setChecked(True)
        
# # #         radio_style = """
# # #             QRadioButton {
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-size: 12px;
# # #                 color: #4C1D95; /* Muted Velvet Slate */
# # #                 background: transparent;
# # #             }
# # #             QRadioButton::indicator {
# # #                 width: 14px;
# # #                 height: 14px;
# # #                 border: 1px solid rgba(109, 40, 217, 0.3);
# # #                 border-radius: 7px;
# # #                 background: white;
# # #             }
# # #             QRadioButton::indicator:checked {
# # #                 background-color: #EC4899; /* Active Rose */
# # #                 border-color: #EC4899;
# # #             }
# # #         """
# # #         self.rad_email.setStyleSheet(radio_style)
# # #         self.rad_bluetooth.setStyleSheet(radio_style)
# # #         self.rad_print.setStyleSheet(radio_style)
        
# # #         self.export_group.addButton(self.rad_email)
# # #         self.export_group.addButton(self.rad_bluetooth)
# # #         self.export_group.addButton(self.rad_print)
        
# # #         self.left_layout.addWidget(self.rad_email)
# # #         self.left_layout.addWidget(self.rad_bluetooth)
# # #         self.left_layout.addWidget(self.rad_print)
        
# # #         self.t_sender_email = QLineEdit()
# # #         self.t_sender_email.setText("oncovuevision@gmail.com")
# # #         self.t_sender_email.setPlaceholderText("Your Gmail Address")
# # #         self.t_sender_email.setStyleSheet(input_style)
# # #         self.left_layout.addWidget(self.t_sender_email)
        
# # #         self.t_sender_pass = QLineEdit()
# # #         self.t_sender_pass.setPlaceholderText("Your App Password (16-character)")
# # #         self.t_sender_pass.setEchoMode(QLineEdit.EchoMode.Password)
# # #         self.t_sender_pass.setStyleSheet(input_style)
# # #         self.left_layout.addWidget(self.t_sender_pass)
        
# # #         self.t_email = QLineEdit()
# # #         self.t_email.setPlaceholderText("Recipient Email Address")
# # #         self.t_email.setStyleSheet(input_style)
# # #         self.left_layout.addWidget(self.t_email)
        
# # #         # Primary Action Button
# # #         self.btn_export = QPushButton("Export Now")
# # #         self.btn_export.setMinimumHeight(45)
# # #         self.btn_export.setStyleSheet("""
# # #             QPushButton {
# # #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
# # #                     stop:0 #EC4899, 
# # #                     stop:1 #6D28D9); /* Rose to Orchid gradient */
# # #                 color: white;
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-weight: bold;
# # #                 border: none;
# # #                 border-radius: 8px;
# # #                 font-size: 14px;
# # #             }
# # #             QPushButton:hover {
# # #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
# # #                     stop:0 #F472B6, 
# # #                     stop:1 #7C3AED);
# # #             }
# # #             QPushButton:pressed {
# # #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
# # #                     stop:0 #DB2777, 
# # #                     stop:1 #5B21B6);
# # #             }
# # #         """)
# # #         self.btn_export.clicked.connect(self.execute_export)
# # #         self.left_layout.addWidget(self.btn_export)
        
# # #         # Status Notification Label
# # #         self.status_label = QLabel("")
# # #         self.status_label.setWordWrap(True)
# # #         self.status_label.setStyleSheet("""
# # #             font-family: 'Poppins', sans-serif;
# # #             color: #EF4444; /* Soft Crimson warning accent */
# # #             font-weight: bold;
# # #             font-size: 16px;
# # #             background: transparent;
# # #         """)
# # #         self.left_layout.addWidget(self.status_label)
# # #         self.left_layout.addStretch()

# # #     def setup_right_panel(self):
# # #         # Embed QScrollArea inside the container seamlessly
# # #         self.scroll_area = QScrollArea()
# # #         self.scroll_area.setWidgetResizable(True)
# # #         self.scroll_area.setStyleSheet("""
# # #             QScrollArea {
# # #                 border: none;
# # #                 background-color: transparent;
# # #             }
# # #         """)
        
# # #         self.scroll_content = QWidget()
# # #         self.scroll_content.setStyleSheet("background-color: transparent;")
# # #         self.scroll_layout = QVBoxLayout(self.scroll_content)
# # #         self.scroll_layout.setContentsMargins(5, 5, 5, 5)
# # #         self.scroll_layout.setSpacing(15)
# # #         self.scroll_area.setWidget(self.scroll_content)
# # #         self.right_layout.addWidget(self.scroll_area)
        
# # #         # Text Browser styling QSS rules
# # #         browser_style = """
# # #             QTextBrowser {
# # #                 background-color: rgba(255, 255, 255, 0.85);
# # #                 border: 1px solid rgba(109, 40, 217, 0.15);
# # #                 border-radius: 8px;
# # #                 padding: 15px;
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-size: 13px;
# # #                 color: #2E1065; /* Deep Amethyst */
# # #             }
# # #         """
        
# # #         self.info_display = QTextBrowser()
# # #         self.info_display.setPlaceholderText("Patient clinical data will appear here...")
# # #         self.info_display.setFixedHeight(180)
# # #         self.info_display.setStyleSheet(browser_style)
# # #         self.scroll_layout.addWidget(self.info_display)
        
# # #         # Diagnostic display graphic placeholder box
# # #         self.image_display = QLabel()
# # #         self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
# # #         self.image_display.setStyleSheet("""
# # #             QLabel {
# # #                 border: 2px dashed rgba(109, 40, 217, 0.18);
# # #                 border-radius: 8px;
# # #                 background-color: rgba(255, 255, 255, 0.4);
# # #                 color: #4C1D95;
# # #                 font-family: 'Poppins', 'Inter', sans-serif;
# # #                 font-size: 12px;
# # #                 min-height: 200px;
# # #             }
# # #         """)
# # #         self.scroll_layout.addWidget(self.image_display)
        
# # #         self.report_display = QTextBrowser()
# # #         self.report_display.setPlaceholderText("Report document contents/PDF view...")
# # #         self.report_display.setFixedHeight(180)
# # #         self.report_display.setStyleSheet(browser_style)
# # #         self.scroll_layout.addWidget(self.report_display)

# # #     def search_patient(self):
# # #         self.status_label.clear()
# # #         self.info_display.clear()
# # #         self.image_display.clear()
# # #         self.report_display.clear()
# # #         self.selected_patient = None
        
# # #         name_q = self.s_name.text().strip().lower()
# # #         gender_q = self.s_gender.currentText().strip().lower()
# # #         age_q = self.s_age.text().strip().lower()
# # #         doctor_q = self.s_doctor.currentText().strip().lower()
        
# # #         if not os.path.exists(self.data_file):
# # #             self.status_label.setText("Exception: Patient data file not found.")
# # #             return
            
# # #         found_data = []
# # #         try:
# # #             wb = openpyxl.load_workbook(self.data_file, data_only=True)
# # #             sheet = wb.active
# # #             headers = [str(cell.value).strip().lower() for cell in sheet[1]]
            
# # #             for row in sheet.iter_rows(min_row=2, values_only=True):
# # #                 if not any(x is not None for x in row):
# # #                     continue
# # #                 row_dict = {headers[i]: row[i] for i in range(len(headers)) if i < len(row)}
                
# # #                 p_name = str(row_dict.get("patien_name", "")).strip().lower()
# # #                 p_gender = str(row_dict.get("gender", "")).strip().lower()
# # #                 p_age = str(row_dict.get("age", "")).strip().lower()
# # #                 p_doctor = str(row_dict.get("doctor", "")).strip().lower()
                
# # #                 match = True
# # #                 if name_q and name_q not in p_name:
# # #                     match = False
# # #                 if gender_q != "select gender" and gender_q != p_gender:
# # #                     match = False
# # #                 if age_q and age_q != p_age:
# # #                     match = False
# # #                 if doctor_q != "select doctor" and doctor_q != p_doctor:
# # #                     match = False
                    
# # #                 if match:
# # #                     found_data.append(row_dict)
# # #             wb.close()
# # #         except Exception as e:
# # #             self.status_label.setText(f"Exception: {str(e)}")
# # #             return
            
# # #         if not found_data:
# # #             self.status_label.setText("Exception: No such patient data found.")
# # #             return
            
# # #         self.selected_patient = found_data[0]
# # #         self.display_patient_details(self.selected_patient)

# # #     def display_patient_details(self, data):
# # #         info_text = f"<b>Patient Details</b><br>"
# # #         for k, v in data.items():
# # #             if k not in ["image_path", "report_path"]:
# # #                 info_text += f"<b>{k.replace('_', ' ').title()}:</b> {v}<br>"
# # #         self.info_display.setHtml(info_text)
        
# # #         img_path = str(data.get("image_path", "")).strip()
# # #         if img_path and os.path.exists(img_path):
# # #             pixmap = QPixmap(img_path)
# # #             scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
# # #             self.image_display.setPixmap(scaled_pixmap)
# # #         else:
# # #             self.image_display.setText("Image not available/found at path.")
            
# # #         rep_path = str(data.get("report_path", "")).strip()
# # #         if rep_path and os.path.exists(rep_path):
# # #             if rep_path.endswith(".pdf"):
# # #                 self.load_pdf_report(rep_path)
# # #             elif rep_path.endswith(".txt"):
# # #                 try:
# # #                     with open(rep_path, "r", encoding="utf-8") as f:
# # #                         self.report_display.setText(f.read())
# # #                 except Exception:
# # #                     self.report_display.setText("Error loading report text details.")
# # #             else:
# # #                 self.report_display.setText(f"Report path available: {rep_path}\nFile preview restricted inside window.")
# # #         else:
# # #             self.report_display.setText("Report document not available/found at path.")

# # #     def load_pdf_report(self, filepath):
# # #         try:
# # #             import pypdf
# # #             reader = pypdf.PdfReader(filepath)
# # #             text = ""
# # #             for page in reader.pages:
# # #                 extracted = page.extract_text()
# # #                 if extracted:
# # #                     text += extracted + "\n"
# # #             if text.strip():
# # #                 self.report_display.setText(text)
# # #             else:
# # #                 self.report_display.setText("PDF Loaded, but no extractable text content was found.")
# # #         except ImportError:
# # #             self.report_display.setText("To view PDF reports directly, install the required library:\n\npip install pypdf")
# # #         except Exception as e:
# # #             self.report_display.setText(f"Error parsing PDF: {str(e)}")

# # #     def has_internet(self):
# # #         try:
# # #             socket.setdefaulttimeout(3)
# # #             socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
# # #             return True
# # #         except socket.error:
# # #             return False

# # #     def check_wifi(self):
# # #         try:
# # #             hostname = socket.gethostname()
# # #             ip_address = socket.gethostbyname(hostname)
# # #             if ip_address.startswith("127."):
# # #                 return False
# # #             return True
# # #         except Exception:
# # #             return False

# # #     def validate_email(self, email):
# # #         pattern = r"^[^@]+@[^@]+\.[^@]+$"
# # #         return bool(re.match(pattern, email))

# # #     def execute_export(self):
# # #         self.status_label.clear()
# # #         if not self.selected_patient:
# # #             self.status_label.setText("Error: Load and select patient details first.")
# # #             return
            
# # #         if self.rad_email.isChecked():
# # #             self.export_via_email()
# # #         elif self.rad_bluetooth.isChecked():
# # #             self.export_via_bluetooth()
# # #         elif self.rad_print.isChecked():
# # #             self.export_via_print()

# # #     # def export_via_email(self):
# # #     #     sender_email = "oncovuevision@gmail.com"
# # #     #     sender_password = "hfix fxjp nvhh diwe"
# # #     #     email_to = self.t_email.text().strip()
        
# # #     #     if not self.validate_email(sender_email):
# # #     #         self.status_label.setText("Error: Invalid sender email address.")
# # #     #         return
            
# # #     #     if not sender_password:
# # #     #         self.status_label.setText("Error: Sender App Password is required.")
# # #     #         return
            
# # #     #     if not self.validate_email(email_to):
# # #     #         self.status_label.setText("Error: Invalid recipient email id.")
# # #     #         return
            
# # #     #     if not self.has_internet():
# # #     #         self.status_label.setText("Error: No internet connection.")
# # #     #         return
            
# # #     #     try:
# # #     #         msg = MIMEMultipart()
# # #     #         msg['From'] = sender_email
# # #     #         msg['To'] = email_to
# # #     #         msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
# # #     #         body = "Please find attached clinical record data, images, and report documents.\n\n"
# # #     #         for k, v in self.selected_patient.items():
# # #     #             if k not in ["image_path", "report_path"]:
# # #     #                 body += f"{k.title()}: {v}\n"
                    
# # #     #         msg.attach(MIMEText(body, 'plain'))
            
# # #     #         img_path = str(self.selected_patient.get("image_path", "")).strip()
# # #     #         if img_path and os.path.exists(img_path):
# # #     #             with open(img_path, "rb") as attachment:
# # #     #                 part = MIMEBase("application", "octet-stream")
# # #     #                 part.set_payload(attachment.read())
# # #     #                 encoders.encode_base64(part)
# # #     #                 part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
# # #     #                 msg.attach(part)
                    
# # #     #         rep_path = str(self.selected_patient.get("report_path", "")).strip()
# # #     #         if rep_path and os.path.exists(rep_path):
# # #     #             with open(rep_path, "rb") as attachment:
# # #     #                 part = MIMEBase("application", "octet-stream")
# # #     #                 part.set_payload(attachment.read())
# # #     #                 encoders.encode_base64(part)
# # #     #                 part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
# # #     #                 msg.attach(part)
                    
# # #     #         server = smtplib.SMTP("smtp.gmail.com", 587)
# # #     #         server.starttls()
# # #     #         server.login(sender_email, sender_password)
# # #     #         server.send_message(msg)
# # #     #         server.quit()
            
# # #     #         self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-weight: bold;")
# # #     #         self.status_label.setText("Success: Email sent successfully.")
# # #     #     except Exception as e:
# # #     #         self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
# # #     #         self.status_label.setText(f"Error: {str(e)}")

# # #     def export_via_email(self):
# # #         sender_email = "oncovuevision@gmail.com"
# # #         sender_password = "hfix fxjp nvhh diwe"
# # #         email_to = self.t_email.text().strip()
        
# # #         if not self.validate_email(sender_email):
# # #             self.status_label.setText("Error: Invalid sender email address.")
# # #             return
            
# # #         if not sender_password:
# # #             self.status_label.setText("Error: Sender App Password is required.")
# # #             return
            
# # #         if not self.validate_email(email_to):
# # #             self.status_label.setText("Error: Invalid recipient email id.")
# # #             return
            
# # #         if not self.has_internet():
# # #             self.status_label.setText("Error: No internet connection.")
# # #             return
            
# # #         try:
# # #             msg = MIMEMultipart()
# # #             msg['From'] = sender_email
# # #             msg['To'] = email_to
# # #             msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
# # #             body = "Please find attached clinical record data, images, and report documents.\n\n"
# # #             for k, v in self.selected_patient.items():
# # #                 if k not in ["image_path", "report_path"]:
# # #                     body += f"{k.title()}: {v}\n"
                    
# # #             msg.attach(MIMEText(body, 'plain'))
            
# # #             img_path = str(self.selected_patient.get("image_path", "")).strip()
# # #             if img_path and os.path.exists(img_path):
# # #                 with open(img_path, "rb") as attachment:
# # #                     part = MIMEBase("application", "octet-stream")
# # #                     part.set_payload(attachment.read())
# # #                     encoders.encode_base64(part)
# # #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
# # #                     msg.attach(part)
                    
# # #             rep_path = str(self.selected_patient.get("report_path", "")).strip()
# # #             if rep_path and os.path.exists(rep_path):
# # #                 with open(rep_path, "rb") as attachment:
# # #                     part = MIMEBase("application", "octet-stream")
# # #                     part.set_payload(attachment.read())
# # #                     encoders.encode_base64(part)
# # #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
# # #                     msg.attach(part)
            
# # #             try:
# # #                 server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
# # #                 server.login(sender_email, sender_password)
# # #                 server.send_message(msg)
# # #                 server.quit()
# # #             except Exception:
# # #                 server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
# # #                 server.starttls()
# # #                 server.login(sender_email, sender_password)
# # #                 server.send_message(msg)
# # #                 server.quit()
                
# # #             self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
# # #             self.status_label.setText("Success: Email sent successfully.")
# # #         except Exception as e:
# # #             self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
# # #             self.status_label.setText(f"Error: {str(e)}")

# # #     def export_via_bluetooth(self):
# # #         is_bluetooth_active = False
# # #         if sys.platform.startswith("linux"):
# # #             try:
# # #                 output = subprocess.check_output(["hciconfig"], stderr=subprocess.STDOUT)
# # #                 if b"UP RUNNING" in output:
# # #                     is_bluetooth_active = True
# # #             except Exception:
# # #                 pass
# # #         elif sys.platform.startswith("win32"):
# # #             try:
# # #                 import winreg
# # #                 path = r"SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters"
# # #                 key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
# # #                 winreg.CloseKey(key)
# # #                 is_bluetooth_active = True
# # #             except Exception:
# # #                 pass
                
# # #         if not is_bluetooth_active:
# # #             self.status_label.setText("Error: No Bluetooth device hardware found or turned off.")
# # #             return
            
# # #         try:
# # #             patient_name = self.selected_patient.get('patien_name', 'Patient')
# # #             data_to_send = f"Patient: {patient_name}\n"
# # #             for k, v in self.selected_patient.items():
# # #                 if k not in ["image_path", "report_path"]:
# # #                     data_to_send += f"{k}: {v}\n"
                    
# # #             sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# # #             nearby_devices = socket.BluetoothSocket(socket.RFCOMM)
# # #             self.status_label.setText("Scanning for paired RFCOMM Bluetooth devices...")
# # #         except AttributeError:
# # #             self.status_label.setText("Error: System Bluetooth Stack / Python RFCOMM sockets unsupported.")
# # #             return
# # #         except Exception as e:
# # #             self.status_label.setText(f"Error: {str(e)}")
# # #             return
            
# # #         self.status_label.setText("Error: No matched/paired destination Bluetooth device found.")

# # #     def export_via_print(self):
# # #         available_printers = QPrinterInfo.availablePrinters()
# # #         if not available_printers and not self.check_wifi():
# # #             self.status_label.setText("Error: No Wi-Fi connection and no local USB printer detected.")
# # #             return
            
# # #         printer = QPrinter()
# # #         dialog = QPrintDialog(printer, self)
# # #         if dialog.exec() == QPrintDialog.DialogCode.Accepted:
# # #             self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-weight: bold;")
# # #             self.status_label.setText("Success: Sent to print queue.")
# # #         else:
# # #             self.status_label.setText("Error: No printer device found or printing canceled.")

# # # if __name__ == "__main__":
# # #     app = QApplication(sys.argv)
# # #     window = ExportPage()
# # #     window.showFullScreen()
# # #     window.show()
# # #     sys.exit(app.exec())

# # import sys
# # import os
# # import re
# # import socket
# # import smtplib
# # import subprocess
# # import openpyxl
# # from email.mime.multipart import MIMEMultipart
# # from email.mime.text import MIMEText
# # from email.mime.base import MIMEBase
# # from email import encoders
# # from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
# #                              QHBoxLayout, QWidget, QLineEdit, QPushButton, 
# #                              QComboBox, QScrollArea, QTextBrowser, QRadioButton, QButtonGroup, QGraphicsDropShadowEffect)
# # from PyQt6.QtCore import Qt
# # from PyQt6.QtGui import QPixmap, QColor
# # from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
# # from keyboard import VirtualKeyboard

# # class ExportPage(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("OncoVue - Export Patient Data")
# #         self.setFixedSize(1280, 720)
        
# #         self.data_file = r"data/data.xlsx"
# #         self.user_file = r"data/user.xlsx"
# #         self.selected_patient = None
        
# #         # Central Widget & Background Setup (Soft Pastel Gradient Base)
# #         self.central_widget = QWidget()
# #         self.central_widget.setObjectName("CentralWidget")
# #         self.central_widget.setStyleSheet("""
# #             #CentralWidget {
# #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
# #                     stop:0 #FAF7FF, 
# #                     stop:0.6 #F3E8FF, 
# #                     stop:1 #E9D5FF);
# #             }
# #         """)
# #         self.setCentralWidget(self.central_widget)
        
# #         # Master Vertical Layout
# #         self.main_layout = QVBoxLayout(self.central_widget)
# #         self.main_layout.setContentsMargins(25, 20, 25, 20)
# #         self.main_layout.setSpacing(15)
        
# #         # Top Navigation Bar Layout (Glass Back Button)
# #         self.top_bar = QHBoxLayout()
# #         self.btn_back = QPushButton("← Back")
# #         self.btn_back.setFixedSize(110, 38)
# #         self.btn_back.setStyleSheet("""
# #             QPushButton {
# #                 background-color: rgba(109, 40, 217, 0.08);
# #                 border: 1px solid rgba(109, 40, 217, 0.18);
# #                 color: #4C1D95; /* Velvet Slate */
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-weight: bold;
# #                 border-radius: 8px;
# #                 font-size: 13px;
# #             }
# #             QPushButton:hover {
# #                 background-color: rgba(109, 40, 217, 0.15);
# #                 border-color: rgba(109, 40, 217, 0.3);
# #             }
# #             QPushButton:pressed {
# #                 background-color: rgba(109, 40, 217, 0.25);
# #             }
# #         """)
# #         self.btn_back.clicked.connect(self.back_to_dashboard)
# #         self.top_bar.addWidget(self.btn_back)
# #         self.top_bar.addStretch()
# #         self.main_layout.addLayout(self.top_bar)
        
# #         # Split workspace layouts
# #         self.content_layout = QHBoxLayout()
# #         self.main_layout.addLayout(self.content_layout)
        
# #         # Left Panel (Frosted Glass Container for inputs)
# #         self.left_panel = QWidget()
# #         self.left_panel.setObjectName("LeftPanel")
# #         self.left_panel.setFixedWidth(390)
# #         self.left_panel.setStyleSheet("""
# #             #LeftPanel {
# #                 background-color: rgba(255, 255, 255, 0.72);
# #                 border: 1px solid rgba(109, 40, 217, 0.15);
# #                 border-radius: 16px;
# #             }
# #         """)
        
# #         # Left Panel Shadow
# #         shadow_left = QGraphicsDropShadowEffect(self)
# #         shadow_left.setBlurRadius(25)
# #         shadow_left.setColor(QColor(109, 40, 217, 15))
# #         shadow_left.setOffset(0, 8)
# #         self.left_panel.setGraphicsEffect(shadow_left)
        
# #         self.left_layout = QVBoxLayout(self.left_panel)
# #         self.left_layout.setSpacing(12)
# #         self.left_layout.setContentsMargins(25, 25, 25, 25)
# #         self.content_layout.addWidget(self.left_panel)
        
# #         # Right Panel (Frosted Glass Container for data view)
# #         self.right_panel = QWidget()
# #         self.right_panel.setObjectName("RightPanel")
# #         self.right_panel.setStyleSheet("""
# #             #RightPanel {
# #                 background-color: rgba(255, 255, 255, 0.72);
# #                 border: 1px solid rgba(109, 40, 217, 0.15);
# #                 border-radius: 16px;
# #             }
# #         """)
        
# #         # Right Panel Shadow
# #         shadow_right = QGraphicsDropShadowEffect(self)
# #         shadow_right.setBlurRadius(25)
# #         shadow_right.setColor(QColor(109, 40, 217, 15))
# #         shadow_right.setOffset(0, 8)
# #         self.right_panel.setGraphicsEffect(shadow_right)
        
# #         self.right_layout = QVBoxLayout(self.right_panel)
# #         self.right_layout.setContentsMargins(15, 15, 15, 15)
# #         self.content_layout.addWidget(self.right_panel)
        
# #         self.setup_left_panel()
# #         self.setup_right_panel()
# #         self.keyboard = VirtualKeyboard(self)
# #         self.keyboard.show()
# #         self.keyboard.move(100, 480)
        

# #     def back_to_dashboard(self):
# #                 # self.timer.stop()
# #         subprocess.Popen([sys.executable, "loader.py"])
# #         subprocess.Popen([sys.executable, "page3.py"])
# #         self.close()

# #     def get_doctors_list(self):
# #         doctors = ["Select Doctor"]
# #         if os.path.exists(self.user_file):
# #             try:
# #                 wb = openpyxl.load_workbook(self.user_file, data_only=True)
# #                 sheet = wb.active
# #                 for row in sheet.iter_rows(min_row=2, values_only=True):
# #                     if len(row) >= 2 and row[1]:
# #                         doc_name = str(row[1]).strip()
# #                         if doc_name not in doctors:
# #                             doctors.append(doc_name)
# #                 wb.close()
# #             except Exception:
# #                 pass
# #         return doctors

# #     def setup_left_panel(self):
# #         # Section Header Label
# #         lbl_search_title = QLabel("SEARCH PATIENT DATA")
# #         lbl_search_title.setStyleSheet("""
# #             font-family: 'Poppins', 'Inter', sans-serif;
# #             font-size: 11px;
# #             font-weight: bold;
# #             color: #6D28D9; /* Orchid Purple */
# #             letter-spacing: 2px;
# #             background: transparent;
# #         """)
# #         self.left_layout.addWidget(lbl_search_title)
        
# #         self.s_name = QLineEdit()
# #         self.s_name.setPlaceholderText("Patient Name")
        
# #         self.s_gender = QComboBox()
# #         self.s_gender.addItems(["Select Gender", "Female"])
        
# #         self.s_age = QLineEdit()
# #         self.s_age.setPlaceholderText("Age")
        
# #         self.s_doctor = QComboBox()
# #         self.s_doctor.addItems(self.get_doctors_list())
        
# #         input_style = """
# #             QLineEdit, QComboBox {
# #                 border: 1px solid rgba(109, 40, 217, 0.18);
# #                 border-radius: 6px;
# #                 padding: 8px 12px;
# #                 background-color: rgba(255, 255, 255, 0.9);
# #                 color: #2E1065; /* Deep Amethyst */
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-size: 13px;
# #             }
# #             QLineEdit:focus, QComboBox:focus {
# #                 border: 1.5px solid #6D28D9;
# #                 background-color: #ffffff;
# #             }
# #         """
# #         self.s_name.setStyleSheet(input_style)
# #         self.s_gender.setStyleSheet(input_style)
# #         self.s_age.setStyleSheet(input_style)
# #         self.s_doctor.setStyleSheet(input_style)
        
# #         self.left_layout.addWidget(self.s_name)
# #         self.left_layout.addWidget(self.s_gender)
# #         self.left_layout.addWidget(self.s_age)
# #         self.left_layout.addWidget(self.s_doctor)
        
# #         self.btn_search = QPushButton("Search Patient")
# #         self.btn_search.setMinimumHeight(38)
# #         self.btn_search.setStyleSheet("""
# #             QPushButton {
# #                 background-color: #6D28D9; /* Solid Orchid Purple */
# #                 color: white;
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-weight: bold;
# #                 border: none;
# #                 border-radius: 6px;
# #                 font-size: 13px;
# #             }
# #             QPushButton:hover {
# #                 background-color: #7C3AED;
# #             }
# #         """)
# #         self.btn_search.clicked.connect(self.search_patient)
# #         self.left_layout.addWidget(self.btn_search)
        
# #         # Export Option Section Header
# #         lbl_export_title = QLabel("EXPORT OPTIONS")
# #         lbl_export_title.setStyleSheet("""
# #             font-family: 'Poppins', 'Inter', sans-serif;
# #             font-size: 11px;
# #             font-weight: bold;
# #             color: #6D28D9;
# #             letter-spacing: 2px;
# #             background: transparent;
# #             margin-top: 10px;
# #         """)
# #         self.left_layout.addWidget(lbl_export_title)
        
# #         self.export_group = QButtonGroup(self)
        
# #         self.rad_email = QRadioButton("Export via Email")
# #         self.rad_bluetooth = QRadioButton("Export via Bluetooth")
# #         self.rad_print = QRadioButton("Print to Printer (USB / Wi-Fi)")
# #         self.rad_email.setChecked(True)
        
# #         radio_style = """
# #             QRadioButton {
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-size: 12px;
# #                 color: #4C1D95; /* Muted Velvet Slate */
# #                 background: transparent;
# #             }
# #             QRadioButton::indicator {
# #                 width: 14px;
# #                 height: 14px;
# #                 border: 1px solid rgba(109, 40, 217, 0.3);
# #                 border-radius: 7px;
# #                 background: white;
# #             }
# #             QRadioButton::indicator:checked {
# #                 background-color: #EC4899; /* Active Rose */
# #                 border-color: #EC4899;
# #             }
# #         """
# #         self.rad_email.setStyleSheet(radio_style)
# #         self.rad_bluetooth.setStyleSheet(radio_style)
# #         self.rad_print.setStyleSheet(radio_style)
        
# #         self.export_group.addButton(self.rad_email)
# #         self.export_group.addButton(self.rad_bluetooth)
# #         self.export_group.addButton(self.rad_print)
        
# #         self.left_layout.addWidget(self.rad_email)
# #         self.left_layout.addWidget(self.rad_bluetooth)
# #         self.left_layout.addWidget(self.rad_print)
        
# #         self.t_sender_email = QLineEdit()
# #         self.t_sender_email.setText("oncovuevision@gmail.com")
# #         self.t_sender_email.setPlaceholderText("Your Gmail Address")
# #         self.t_sender_email.setStyleSheet(input_style)
# #         self.left_layout.addWidget(self.t_sender_email)
        
# #         self.t_sender_pass = QLineEdit()
# #         self.t_sender_pass.setPlaceholderText("Your App Password (16-character)")
# #         self.t_sender_pass.setEchoMode(QLineEdit.EchoMode.Password)
# #         self.t_sender_pass.setStyleSheet(input_style)
# #         self.left_layout.addWidget(self.t_sender_pass)
        
# #         self.t_email = QLineEdit()
# #         self.t_email.setPlaceholderText("Recipient Email Address")
# #         self.t_email.setStyleSheet(input_style)
# #         self.left_layout.addWidget(self.t_email)
        
# #         # Primary Action Button
# #         self.btn_export = QPushButton("Export Now")
# #         self.btn_export.setMinimumHeight(45)
# #         self.btn_export.setStyleSheet("""
# #             QPushButton {
# #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
# #                     stop:0 #EC4899, 
# #                     stop:1 #6D28D9); /* Rose to Orchid gradient */
# #                 color: white;
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-weight: bold;
# #                 border: none;
# #                 border-radius: 8px;
# #                 font-size: 14px;
# #             }
# #             QPushButton:hover {
# #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
# #                     stop:0 #F472B6, 
# #                     stop:1 #7C3AED);
# #             }
# #             QPushButton:pressed {
# #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
# #                     stop:0 #DB2777, 
# #                     stop:1 #5B21B6);
# #             }
# #         """)
# #         self.btn_export.clicked.connect(self.execute_export)
# #         self.left_layout.addWidget(self.btn_export)
        
# #         # Status Notification Label
# #         self.status_label = QLabel("")
# #         self.status_label.setWordWrap(True)
# #         self.status_label.setStyleSheet("""
# #             font-family: 'Poppins', sans-serif;
# #             color: #EF4444; /* Soft Crimson warning accent */
# #             font-weight: bold;
# #             font-size: 16px;
# #             background: transparent;
# #         """)
# #         self.left_layout.addWidget(self.status_label)
# #         self.left_layout.addStretch()

# #     def setup_right_panel(self):
# #         # Embed QScrollArea inside the container seamlessly
# #         self.scroll_area = QScrollArea()
# #         self.scroll_area.setWidgetResizable(True)
# #         self.scroll_area.setStyleSheet("""
# #             QScrollArea {
# #                 border: none;
# #                 background-color: transparent;
# #             }
# #         """)
        
# #         self.scroll_content = QWidget()
# #         self.scroll_content.setStyleSheet("background-color: transparent;")
# #         self.scroll_layout = QVBoxLayout(self.scroll_content)
# #         self.scroll_layout.setContentsMargins(5, 5, 5, 5)
# #         self.scroll_layout.setSpacing(15)
# #         self.scroll_area.setWidget(self.scroll_content)
# #         self.right_layout.addWidget(self.scroll_area)
        
# #         # Text Browser styling QSS rules
# #         browser_style = """
# #             QTextBrowser {
# #                 background-color: rgba(255, 255, 255, 0.85);
# #                 border: 1px solid rgba(109, 40, 217, 0.15);
# #                 border-radius: 8px;
# #                 padding: 15px;
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-size: 13px;
# #                 color: #2E1065; /* Deep Amethyst */
# #             }
# #         """
        
# #         self.info_display = QTextBrowser()
# #         self.info_display.setPlaceholderText("Patient clinical data will appear here...")
# #         self.info_display.setFixedHeight(180)
# #         self.info_display.setStyleSheet(browser_style)
# #         self.scroll_layout.addWidget(self.info_display)
        
# #         # Diagnostic display graphic placeholder box
# #         self.image_display = QLabel()
# #         self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
# #         self.image_display.setStyleSheet("""
# #             QLabel {
# #                 border: 2px dashed rgba(109, 40, 217, 0.18);
# #                 border-radius: 8px;
# #                 background-color: rgba(255, 255, 255, 0.4);
# #                 color: #4C1D95;
# #                 font-family: 'Poppins', 'Inter', sans-serif;
# #                 font-size: 12px;
# #                 min-height: 200px;
# #             }
# #         """)
# #         self.scroll_layout.addWidget(self.image_display)
        
# #         self.report_display = QTextBrowser()
# #         self.report_display.setPlaceholderText("Report document contents/PDF view...")
# #         self.report_display.setFixedHeight(180)
# #         self.report_display.setStyleSheet(browser_style)
# #         self.scroll_layout.addWidget(self.report_display)

# #     def search_patient(self):
# #         self.status_label.clear()
# #         self.info_display.clear()
# #         self.image_display.clear()
# #         self.report_display.clear()
# #         self.selected_patient = None
        
# #         name_q = self.s_name.text().strip().lower()
# #         gender_q = self.s_gender.currentText().strip().lower()
# #         age_q = self.s_age.text().strip().lower()
# #         doctor_q = self.s_doctor.currentText().strip().lower()
        
# #         if not os.path.exists(self.data_file):
# #             self.status_label.setText("Exception: Patient data file not found.")
# #             return
            
# #         found_data = []
# #         try:
# #             wb = openpyxl.load_workbook(self.data_file, data_only=True)
# #             sheet = wb.active
# #             headers = [str(cell.value).strip().lower() for cell in sheet[1]]
            
# #             for row in sheet.iter_rows(min_row=2, values_only=True):
# #                 if not any(x is not None for x in row):
# #                     continue
# #                 row_dict = {headers[i]: row[i] for i in range(len(headers)) if i < len(row)}
                
# #                 p_name = str(row_dict.get("patien_name", "")).strip().lower()
# #                 p_gender = str(row_dict.get("gender", "")).strip().lower()
# #                 p_age = str(row_dict.get("age", "")).strip().lower()
# #                 p_doctor = str(row_dict.get("doctor", "")).strip().lower()
                
# #                 match = True
# #                 if name_q and name_q not in p_name:
# #                     match = False
# #                 if gender_q != "select gender" and gender_q != p_gender:
# #                     match = False
# #                 if age_q and age_q != p_age:
# #                     match = False
# #                 if doctor_q != "select doctor" and doctor_q != p_doctor:
# #                     match = False
                    
# #                 if match:
# #                     found_data.append(row_dict)
# #             wb.close()
# #         except Exception as e:
# #             self.status_label.setText(f"Exception: {str(e)}")
# #             return
            
# #         if not found_data:
# #             self.status_label.setText("Exception: No such patient data found.")
# #             return
            
# #         self.selected_patient = found_data[0]
# #         self.display_patient_details(self.selected_patient)

# #     def display_patient_details(self, data):
# #         info_text = f"<b>Patient Details</b><br>"
# #         for k, v in data.items():
# #             if k not in ["image_path", "report_path"]:
# #                 info_text += f"<b>{k.replace('_', ' ').title()}:</b> {v}<br>"
# #         self.info_display.setHtml(info_text)
        
# #         img_path = str(data.get("image_path", "")).strip()
# #         if img_path and os.path.exists(img_path):
# #             pixmap = QPixmap(img_path)
# #             scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
# #             self.image_display.setPixmap(scaled_pixmap)
# #         else:
# #             self.image_display.setText("Image not available/found at path.")
            
# #         rep_path = str(data.get("report_path", "")).strip()
# #         if rep_path and os.path.exists(rep_path):
# #             if rep_path.endswith(".pdf"):
# #                 self.load_pdf_report(rep_path)
# #             elif rep_path.endswith(".txt"):
# #                 try:
# #                     with open(rep_path, "r", encoding="utf-8") as f:
# #                         self.report_display.setText(f.read())
# #                 except Exception:
# #                     self.report_display.setText("Error loading report text details.")
# #             else:
# #                 self.report_display.setText(f"Report path available: {rep_path}\nFile preview restricted inside window.")
# #         else:
# #             self.report_display.setText("Report document not available/found at path.")

# #     def load_pdf_report(self, filepath):
# #         try:
# #             import pypdf
# #             reader = pypdf.PdfReader(filepath)
# #             text = ""
# #             for page in reader.pages:
# #                 extracted = page.extract_text()
# #                 if extracted:
# #                     text += extracted + "\n"
# #             if text.strip():
# #                 self.report_display.setText(text)
# #             else:
# #                 self.report_display.setText("PDF Loaded, but no extractable text content was found.")
# #         except ImportError:
# #             self.report_display.setText("To view PDF reports directly, install the required library:\n\npip install pypdf")
# #         except Exception as e:
# #             self.report_display.setText(f"Error parsing PDF: {str(e)}")

# #     def has_internet(self):
# #         try:
# #             socket.setdefaulttimeout(3)
# #             socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
# #             return True
# #         except socket.error:
# #             return False

# #     def check_wifi(self):
# #         try:
# #             hostname = socket.gethostname()
# #             ip_address = socket.gethostbyname(hostname)
# #             if ip_address.startswith("127."):
# #                 return False
# #             return True
# #         except Exception:
# #             return False

# #     def validate_email(self, email):
# #         pattern = r"^[^@]+@[^@]+\.[^@]+$"
# #         return bool(re.match(pattern, email))

# #     def execute_export(self):
# #         self.status_label.clear()
# #         if not self.selected_patient:
# #             self.status_label.setText("Error: Load and select patient details first.")
# #             return
            
# #         if self.rad_email.isChecked():
# #             self.export_via_email()
# #         elif self.rad_bluetooth.isChecked():
# #             self.export_via_bluetooth()
# #         elif self.rad_print.isChecked():
# #             self.export_via_print()

# #     # def export_via_email(self):
# #     #     sender_email = "oncovuevision@gmail.com"
# #     #     sender_password = "hfix fxjp nvhh diwe"
# #     #     email_to = self.t_email.text().strip()
        
# #     #     if not self.validate_email(sender_email):
# #     #         self.status_label.setText("Error: Invalid sender email address.")
# #     #         return
            
# #     #     if not sender_password:
# #     #         self.status_label.setText("Error: Sender App Password is required.")
# #     #         return
            
# #     #     if not self.validate_email(email_to):
# #     #         self.status_label.setText("Error: Invalid recipient email id.")
# #     #         return
            
# #     #     if not self.has_internet():
# #     #         self.status_label.setText("Error: No internet connection.")
# #     #         return
            
# #     #     try:
# #     #         msg = MIMEMultipart()
# #     #         msg['From'] = sender_email
# #     #         msg['To'] = email_to
# #     #         msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
# #     #         body = "Please find attached clinical record data, images, and report documents.\n\n"
# #     #         for k, v in self.selected_patient.items():
# #     #             if k not in ["image_path", "report_path"]:
# #     #                 body += f"{k.title()}: {v}\n"
                    
# #     #         msg.attach(MIMEText(body, 'plain'))
            
# #     #         img_path = str(self.selected_patient.get("image_path", "")).strip()
# #     #         if img_path and os.path.exists(img_path):
# #     #             with open(img_path, "rb") as attachment:
# #     #                 part = MIMEBase("application", "octet-stream")
# #     #                 part.set_payload(attachment.read())
# #     #                 encoders.encode_base64(part)
# #     #                 part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
# #     #                 msg.attach(part)
                    
# #     #         rep_path = str(self.selected_patient.get("report_path", "")).strip()
# #     #         if rep_path and os.path.exists(rep_path):
# #     #             with open(rep_path, "rb") as attachment:
# #     #                 part = MIMEBase("application", "octet-stream")
# #     #                 part.set_payload(attachment.read())
# #     #                 encoders.encode_base64(part)
# #     #                 part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
# #     #                 msg.attach(part)
                    
# #     #         server = smtplib.SMTP("smtp.gmail.com", 587)
# #     #         server.starttls()
# #     #         server.login(sender_email, sender_password)
# #     #         server.send_message(msg)
# #     #         server.quit()
            
# #     #         self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-weight: bold;")
# #     #         self.status_label.setText("Success: Email sent successfully.")
# #     #     except Exception as e:
# #     #         self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
# #     #         self.status_label.setText(f"Error: {str(e)}")

# #     def export_via_email(self):
# #         sender_email = "oncovuevision@gmail.com"
# #         sender_password = "hfix fxjp nvhh diwe"
# #         email_to = self.t_email.text().strip()
        
# #         if not self.validate_email(sender_email):
# #             self.status_label.setText("Error: Invalid sender email address.")
# #             return
            
# #         if not sender_password:
# #             self.status_label.setText("Error: Sender App Password is required.")
# #             return
            
# #         if not self.validate_email(email_to):
# #             self.status_label.setText("Error: Invalid recipient email id.")
# #             return
            
# #         if not self.has_internet():
# #             self.status_label.setText("Error: No internet connection.")
# #             return
            
# #         try:
# #             msg = MIMEMultipart()
# #             msg['From'] = sender_email
# #             msg['To'] = email_to
# #             msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
# #             body = "Please find attached clinical record data, images, and report documents.\n\n"
# #             for k, v in self.selected_patient.items():
# #                 if k not in ["image_path", "report_path"]:
# #                     body += f"{k.title()}: {v}\n"
                    
# #             msg.attach(MIMEText(body, 'plain'))
            
# #             img_path = str(self.selected_patient.get("image_path", "")).strip()
# #             if img_path and os.path.exists(img_path):
# #                 with open(img_path, "rb") as attachment:
# #                     part = MIMEBase("application", "octet-stream")
# #                     part.set_payload(attachment.read())
# #                     encoders.encode_base64(part)
# #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
# #                     msg.attach(part)
                    
# #             rep_path = str(self.selected_patient.get("report_path", "")).strip()
# #             if rep_path and os.path.exists(rep_path):
# #                 with open(rep_path, "rb") as attachment:
# #                     part = MIMEBase("application", "octet-stream")
# #                     part.set_payload(attachment.read())
# #                     encoders.encode_base64(part)
# #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
# #                     msg.attach(part)
            
# #             try:
# #                 server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
# #                 server.login(sender_email, sender_password)
# #                 server.send_message(msg)
# #                 server.quit()
# #             except Exception:
# #                 server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
# #                 server.starttls()
# #                 server.login(sender_email, sender_password)
# #                 server.send_message(msg)
# #                 server.quit()
                
# #             self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
# #             self.status_label.setText("Success: Email sent successfully.")
# #         except Exception as e:
# #             self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
# #             self.status_label.setText(f"Error: {str(e)}")

# #     def export_via_bluetooth(self):
# #         is_bluetooth_active = False
# #         if sys.platform.startswith("linux"):
# #             try:
# #                 output = subprocess.check_output(["hciconfig"], stderr=subprocess.STDOUT)
# #                 if b"UP RUNNING" in output:
# #                     is_bluetooth_active = True
# #             except Exception:
# #                 pass
# #         elif sys.platform.startswith("win32"):
# #             try:
# #                 import winreg
# #                 path = r"SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters"
# #                 key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
# #                 winreg.CloseKey(key)
# #                 is_bluetooth_active = True
# #             except Exception:
# #                 pass
                
# #         if not is_bluetooth_active:
# #             self.status_label.setText("Error: No Bluetooth device hardware found or turned off.")
# #             return
            
# #         try:
# #             patient_name = self.selected_patient.get('patien_name', 'Patient')
# #             data_to_send = f"Patient: {patient_name}\n"
# #             for k, v in self.selected_patient.items():
# #                 if k not in ["image_path", "report_path"]:
# #                     data_to_send += f"{k}: {v}\n"
                    
# #             sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# #             nearby_devices = socket.BluetoothSocket(socket.RFCOMM)
# #             self.status_label.setText("Scanning for paired RFCOMM Bluetooth devices...")
# #         except AttributeError:
# #             self.status_label.setText("Error: System Bluetooth Stack / Python RFCOMM sockets unsupported.")
# #             return
# #         except Exception as e:
# #             self.status_label.setText(f"Error: {str(e)}")
# #             return
            
# #         self.status_label.setText("Error: No matched/paired destination Bluetooth device found.")

# #     def export_via_print(self):
# #         available_printers = QPrinterInfo.availablePrinters()
# #         if not available_printers and not self.check_wifi():
# #             self.status_label.setText("Error: No Wi-Fi connection and no local USB printer detected.")
# #             return
            
# #         printer = QPrinter()
# #         dialog = QPrintDialog(printer, self)
# #         if dialog.exec() == QPrintDialog.DialogCode.Accepted:
# #             self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-weight: bold;")
# #             self.status_label.setText("Success: Sent to print queue.")
# #         else:
# #             self.status_label.setText("Error: No printer device found or printing canceled.")

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = ExportPage()
# #     window.showFullScreen()
# #     window.show()
# #     sys.exit(app.exec())

# import sys
# import os
# import re
# import socket
# import smtplib
# import subprocess
# import openpyxl
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from keyboard import VirtualKeyboard 
# import smtplib
# import ssl

# orig_getaddrinfo = socket.getaddrinfo
# def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
#     if host == "smtp.gmail.com":
#         family = socket.AF_INET
#     return orig_getaddrinfo(host, port, family, type, proto, flags)
# socket.getaddrinfo = patched_getaddrinfo

# from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
#                              QHBoxLayout, QWidget, QLineEdit, QPushButton,
#                              QComboBox, QScrollArea, QTextBrowser, QRadioButton, QButtonGroup, QGraphicsDropShadowEffect)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QPixmap, QColor
# from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo

# class ExportPage(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("OncoVue - Export Patient Data")
#         self.setFixedSize(1280, 720)
       
#         self.data_file = r"data/data.xlsx"
#         self.user_file = r"data/user.xlsx"
#         self.selected_patient = None
       
#         self.central_widget = QWidget()
#         self.central_widget.setObjectName("CentralWidget")
#         self.central_widget.setStyleSheet("""
#             #CentralWidget {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
#                     stop:0 #FAF7FF,
#                     stop:0.6 #F3E8FF,
#                     stop:1 #E9D5FF);
#             }
#         """)
#         self.setCentralWidget(self.central_widget)
       
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(25, 20, 25, 20)
#         self.main_layout.setSpacing(15)
       
#         self.top_bar = QHBoxLayout()
#         self.btn_back = QPushButton("← Back")
#         self.btn_back.setFixedSize(110, 38)
#         self.btn_back.setStyleSheet("""
#             QPushButton {
#                 background-color: rgba(109, 40, 217, 0.08);
#                 border: 1px solid rgba(109, 40, 217, 0.18);
#                 color: #4C1D95; /* Velvet Slate */
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 border-radius: 8px;
#                 font-size: 13px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(109, 40, 217, 0.15);
#                 border-color: rgba(109, 40, 217, 0.3);
#             }
#             QPushButton:pressed {
#                 background-color: rgba(109, 40, 217, 0.25);
#             }
#         """)
#         self.btn_back.clicked.connect(self.back_to_dashboard)
#         self.top_bar.addWidget(self.btn_back)
#         self.top_bar.addStretch()
#         self.main_layout.addLayout(self.top_bar)
       
#         self.content_layout = QHBoxLayout()
#         self.main_layout.addLayout(self.content_layout)
       
#         self.left_panel = QWidget()
#         self.left_panel.setObjectName("LeftPanel")
#         self.left_panel.setFixedWidth(390)
#         self.left_panel.setStyleSheet("""
#             #LeftPanel {
#                 background-color: rgba(255, 255, 255, 0.72);
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 16px;
#             }
#         """)
       
#         shadow_left = QGraphicsDropShadowEffect(self)
#         shadow_left.setBlurRadius(25)
#         shadow_left.setColor(QColor(109, 40, 217, 15))
#         shadow_left.setOffset(0, 8)
#         self.left_panel.setGraphicsEffect(shadow_left)
       
#         self.left_layout = QVBoxLayout(self.left_panel)
#         self.left_layout.setSpacing(12)
#         self.left_layout.setContentsMargins(25, 25, 25, 25)
#         self.content_layout.addWidget(self.left_panel)
       
#         self.right_panel = QWidget()
#         self.right_panel.setObjectName("RightPanel")
#         self.right_panel.setStyleSheet("""
#             #RightPanel {
#                 background-color: rgba(255, 255, 255, 0.72);
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 16px;
#             }
#         """)
       
#         shadow_right = QGraphicsDropShadowEffect(self)
#         shadow_right.setBlurRadius(25)
#         shadow_right.setColor(QColor(109, 40, 217, 15))
#         shadow_right.setOffset(0, 8)
#         self.right_panel.setGraphicsEffect(shadow_right)
       
#         self.right_layout = QVBoxLayout(self.right_panel)
#         self.right_layout.setContentsMargins(15, 15, 15, 15)
#         self.content_layout.addWidget(self.right_panel)
       
#         self.setup_left_panel()
#         self.setup_right_panel()
#         self.keyboard = VirtualKeyboard(self)
#         self.keyboard.show()
#         self.keyboard.move(100, 480)

#     def back_to_dashboard(self):
#         subprocess.Popen([sys.executable, "loader.py"])
#         subprocess.Popen([sys.executable, "page3.py"])
#         self.close()

#     def get_doctors_list(self):
#         doctors = ["Select Doctor"]
#         if os.path.exists(self.user_file):
#             try:
#                 wb = openpyxl.load_workbook(self.user_file, data_only=True)
#                 sheet = wb.active
#                 for row in sheet.iter_rows(min_row=2, values_only=True):
#                     if len(row) >= 2 and row[1]:
#                         doc_name = str(row[1]).strip()
#                         if doc_name not in doctors:
#                             doctors.append(doc_name)
#                 wb.close()
#             except Exception:
#                 pass
#         return doctors

#     def setup_left_panel(self):
#         lbl_search_title = QLabel("SEARCH PATIENT DATA")
#         lbl_search_title.setStyleSheet("""
#             font-family: 'Poppins', 'Inter', sans-serif;
#             font-size: 11px;
#             font-weight: bold;
#             color: #6D28D9; /* Orchid Purple */
#             letter-spacing: 2px;
#             background: transparent;
#         """)
#         self.left_layout.addWidget(lbl_search_title)
       
#         self.s_name = QLineEdit()
#         self.s_name.setPlaceholderText("Patient Name")
       
#         self.s_gender = QComboBox()
#         self.s_gender.addItems(["Select Gender", "Female"])
       
#         self.s_age = QLineEdit()
#         self.s_age.setPlaceholderText("Age")
       
#         self.s_doctor = QComboBox()
#         self.s_doctor.addItems(self.get_doctors_list())
       
#         input_style = """
#             QLineEdit, QComboBox {
#                 border: 1px solid rgba(109, 40, 217, 0.18);
#                 border-radius: 6px;
#                 padding: 8px 12px;
#                 background-color: rgba(255, 255, 255, 0.9);
#                 color: #2E1065; /* Deep Amethyst */
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 13px;
#             }
#             QLineEdit:focus, QComboBox:focus {
#                 border: 1.5px solid #6D28D9;
#                 background-color: #ffffff;
#             }
#         """
#         self.s_name.setStyleSheet(input_style)
#         self.s_gender.setStyleSheet(input_style)
#         self.s_age.setStyleSheet(input_style)
#         self.s_doctor.setStyleSheet(input_style)
       
#         self.left_layout.addWidget(self.s_name)
#         self.left_layout.addWidget(self.s_gender)
#         self.left_layout.addWidget(self.s_age)
#         self.left_layout.addWidget(self.s_doctor)
       
#         self.btn_search = QPushButton("Search Patient")
#         self.btn_search.setMinimumHeight(38)
#         self.btn_search.setStyleSheet("""
#             QPushButton {
#                 background-color: #6D28D9; /* Solid Orchid Purple */
#                 color: white;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 border: none;
#                 border-radius: 6px;
#                 font-size: 13px;
#             }
#             QPushButton:hover {
#                 background-color: #7C3AED;
#             }
#         """)
#         self.btn_search.clicked.connect(self.search_patient)
#         self.left_layout.addWidget(self.btn_search)
       
#         lbl_export_title = QLabel("EXPORT OPTIONS")
#         lbl_export_title.setStyleSheet("""
#             font-family: 'Poppins', 'Inter', sans-serif;
#             font-size: 11px;
#             font-weight: bold;
#             color: #6D28D9;
#             letter-spacing: 2px;
#             background: transparent;
#             margin-top: 10px;
#         """)
#         self.left_layout.addWidget(lbl_export_title)
       
#         self.export_group = QButtonGroup(self)
       
#         self.rad_email = QRadioButton("Export via Email")
#         self.rad_bluetooth = QRadioButton("Export via Bluetooth")
#         self.rad_print = QRadioButton("Print to Printer (USB / Wi-Fi)")
#         self.rad_email.setChecked(True)
       
#         radio_style = """
#             QRadioButton {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 12px;
#                 color: #4C1D95; /* Muted Velvet Slate */
#                 background: transparent;
#             }
#             QRadioButton::indicator {
#                 width: 14px;
#                 height: 14px;
#                 border: 1px solid rgba(109, 40, 217, 0.3);
#                 border-radius: 7px;
#                 background: white;
#             }
#             QRadioButton::indicator:checked {
#                 background-color: #EC4899; /* Active Rose */
#                 border-color: #EC4899;
#             }
#         """
#         self.rad_email.setStyleSheet(radio_style)
#         self.rad_bluetooth.setStyleSheet(radio_style)
#         self.rad_print.setStyleSheet(radio_style)
       
#         self.export_group.addButton(self.rad_email)
#         self.export_group.addButton(self.rad_bluetooth)
#         self.export_group.addButton(self.rad_print)
       
#         self.left_layout.addWidget(self.rad_email)
#         self.left_layout.addWidget(self.rad_bluetooth)
#         self.left_layout.addWidget(self.rad_print)
       
#         self.t_sender_email = QLineEdit()
#         self.t_sender_email.setText("oncovuevision@gmail.com")
#         self.t_sender_email.setPlaceholderText("Your Gmail Address")
#         self.t_sender_email.setStyleSheet(input_style)
#         self.left_layout.addWidget(self.t_sender_email)
       
#         self.t_sender_pass = QLineEdit()
#         self.t_sender_pass.setPlaceholderText("Your App Password (16-character)")
#         self.t_sender_pass.setEchoMode(QLineEdit.EchoMode.Password)
#         self.t_sender_pass.setStyleSheet(input_style)
#         self.left_layout.addWidget(self.t_sender_pass)
       
#         self.t_email = QLineEdit()
#         self.t_email.setPlaceholderText("Recipient Email Address")
#         self.t_email.setStyleSheet(input_style)
#         self.left_layout.addWidget(self.t_email)
       
#         self.btn_export = QPushButton("Export Now")
#         self.btn_export.setMinimumHeight(45)
#         self.btn_export.setStyleSheet("""
#             QPushButton {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
#                     stop:0 #EC4899,
#                     stop:1 #6D28D9); /* Rose to Orchid gradient */
#                 color: white;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 border: none;
#                 border-radius: 8px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
#                     stop:0 #F472B6,
#                     stop:1 #7C3AED);
#             }
#             QPushButton:pressed {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
#                     stop:0 #DB2777,
#                     stop:1 #5B21B6);
#             }
#         """)
#         self.btn_export.clicked.connect(self.execute_export)
#         self.left_layout.addWidget(self.btn_export)
       
#         self.status_label = QLabel("")
#         self.status_label.setWordWrap(True)
#         self.status_label.setStyleSheet("""
#             font-family: 'Poppins', sans-serif;
#             color: #EF4444; /* Soft Crimson warning accent */
#             font-weight: bold;
#             font-size: 16px;
#             background: transparent;
#         """)
#         self.left_layout.addWidget(self.status_label)
#         self.left_layout.addStretch()

#     def setup_right_panel(self):
#         self.scroll_area = QScrollArea()
#         self.scroll_area.setWidgetResizable(True)
#         self.scroll_area.setStyleSheet("""
#             QScrollArea {
#                 border: none;
#                 background-color: transparent;
#             }
#         """)
       
#         self.scroll_content = QWidget()
#         self.scroll_content.setStyleSheet("background-color: transparent;")
#         self.scroll_layout = QVBoxLayout(self.scroll_content)
#         self.scroll_layout.setContentsMargins(5, 5, 5, 5)
#         self.scroll_layout.setSpacing(15)
#         self.scroll_area.setWidget(self.scroll_content)
#         self.right_layout.addWidget(self.scroll_area)
       
#         browser_style = """
#             QTextBrowser {
#                 background-color: rgba(255, 255, 255, 0.85);
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 8px;
#                 padding: 15px;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 13px;
#                 color: #2E1065; /* Deep Amethyst */
#             }
#         """
       
#         self.info_display = QTextBrowser()
#         self.info_display.setPlaceholderText("Patient clinical data will appear here...")
#         self.info_display.setFixedHeight(180)
#         self.info_display.setStyleSheet(browser_style)
#         self.scroll_layout.addWidget(self.info_display)
       
#         self.image_display = QLabel()
#         self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.image_display.setStyleSheet("""
#             QLabel {
#                 border: 2px dashed rgba(109, 40, 217, 0.18);
#                 border-radius: 8px;
#                 background-color: rgba(255, 255, 255, 0.4);
#                 color: #4C1D95;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 12px;
#                 min-height: 200px;
#             }
#         """)
#         self.scroll_layout.addWidget(self.image_display)
       
#         self.report_display = QTextBrowser()
#         self.report_display.setPlaceholderText("Report document contents/PDF view...")
#         self.report_display.setFixedHeight(180)
#         self.report_display.setStyleSheet(browser_style)
#         self.scroll_layout.addWidget(self.report_display)

#     def search_patient(self):
#         self.status_label.clear()
#         self.info_display.clear()
#         self.image_display.clear()
#         self.report_display.clear()
#         self.selected_patient = None
       
#         name_q = self.s_name.text().strip().lower()
#         gender_q = self.s_gender.currentText().strip().lower()
#         age_q = self.s_age.text().strip().lower()
#         doctor_q = self.s_doctor.currentText().strip().lower()
       
#         if not os.path.exists(self.data_file):
#             self.status_label.setText("Exception: Patient data file not found.")
#             return
           
#         found_data = []
#         try:
#             wb = openpyxl.load_workbook(self.data_file, data_only=True)
#             sheet = wb.active
#             headers = [str(cell.value).strip().lower() for cell in sheet[1]]
           
#             for row in sheet.iter_rows(min_row=2, values_only=True):
#                 if not any(x is not None for x in row):
#                     continue
#                 row_dict = {headers[i]: row[i] for i in range(len(headers)) if i < len(row)}
               
#                 p_name = str(row_dict.get("patien_name", "")).strip().lower()
#                 p_gender = str(row_dict.get("gender", "")).strip().lower()
#                 p_age = str(row_dict.get("age", "")).strip().lower()
#                 p_doctor = str(row_dict.get("doctor", "")).strip().lower()
               
#                 match = True
#                 if name_q and name_q not in p_name:
#                     match = False
#                 if gender_q != "select gender" and gender_q != p_gender:
#                     match = False
#                 if age_q and age_q != p_age:
#                     match = False
#                 if doctor_q != "select doctor" and doctor_q != p_doctor:
#                     match = False
                   
#                 if match:
#                     found_data.append(row_dict)
#             wb.close()
#         except Exception as e:
#             self.status_label.setText(f"Exception: {str(e)}")
#             return
           
#         if not found_data:
#             self.status_label.setText("Exception: No such patient data found.")
#             return
           
#         self.selected_patient = found_data[0]
#         self.display_patient_details(self.selected_patient)

#     def display_patient_details(self, data):
#         info_text = f"<b>Patient Details</b><br>"
#         for k, v in data.items():
#             if k not in ["image_path", "report_path"]:
#                 info_text += f"<b>{k.replace('_', ' ').title()}:</b> {v}<br>"
#         self.info_display.setHtml(info_text)
       
#         img_path = str(data.get("image_path", "")).strip()
#         if img_path and os.path.exists(img_path):
#             pixmap = QPixmap(img_path)
#             scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
#             self.image_display.setPixmap(scaled_pixmap)
#         else:
#             self.image_display.setText("Image not available/found at path.")
           
#         rep_path = str(data.get("report_path", "")).strip()
#         if rep_path and os.path.exists(rep_path):
#             if rep_path.endswith(".pdf"):
#                 self.load_pdf_report(rep_path)
#             elif rep_path.endswith(".txt"):
#                 try:
#                     with open(rep_path, "r", encoding="utf-8") as f:
#                         self.report_display.setText(f.read())
#                 except Exception:
#                     self.report_display.setText("Error loading report text details.")
#             else:
#                 self.report_display.setText(f"Report path available: {rep_path}\nFile preview restricted inside window.")
#         else:
#             self.report_display.setText("Report document not available/found at path.")

#     def load_pdf_report(self, filepath):
#         try:
#             import pypdf
#             reader = pypdf.PdfReader(filepath)
#             text = ""
#             for page in reader.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted + "\n"
#             if text.strip():
#                 self.report_display.setText(text)
#             else:
#                 self.report_display.setText("PDF Loaded, but no extractable text content was found.")
#         except ImportError:
#             self.report_display.setText("To view PDF reports directly, install the required library:\n\npip install pypdf")
#         except Exception as e:
#             self.report_display.setText(f"Error parsing PDF: {str(e)}")

#     def has_internet(self):
#         try:
#             socket.setdefaulttimeout(3)
#             socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
#             return True
#         except socket.error:
#             return False

#     def check_wifi(self):
#         try:
#             hostname = socket.gethostname()
#             ip_address = socket.gethostbyname(hostname)
#             if ip_address.startswith("127."):
#                 return False
#             return True
#         except Exception:
#             return False

#     def validate_email(self, email):
#         pattern = r"^[^@]+@[^@]+\.[^@]+$"
#         return bool(re.match(pattern, email))

#     def execute_export(self):
#         self.status_label.clear()
#         if not self.selected_patient:
#             self.status_label.setText("Error: Load and select patient details first.")
#             return
           
#         if self.rad_email.isChecked():
#             self.export_via_email()
#         elif self.rad_bluetooth.isChecked():
#             self.export_via_bluetooth()
#         elif self.rad_print.isChecked():
#             self.export_via_print()

#     def export_via_email(self):
#         sender_email = "oncovuevision@gmail.com"
#         sender_password = "hfix fxjp nvhh diwe"
#         email_to = self.t_email.text().strip()


#         try:
#             context = ssl.create_default_context()
#             print("Attempting connection to smtp.gmail.com...")
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=10) as server:
#                 server.login(sender_email, sender_password)
#                 print("Connection and login successful!")
#         except Exception as e:
#             print(f"Error occurred: {type(e).__name__} - {e}")
       
#         if not self.validate_email(sender_email):
#             self.status_label.setText("Error: Invalid sender email address.")
#             return
           
#         if not sender_password:
#             self.status_label.setText("Error: Sender App Password is required.")
#             return
           
#         if not self.validate_email(email_to):
#             self.status_label.setText("Error: Invalid recipient email id.")
#             return
           
#         if not self.has_internet():
#             self.status_label.setText("Error: No internet connection.")
#             return
        
#         self.status_label.setStyleSheet("color: #6D28D9; font-weight: bold;")
#         self.status_label.setText("Sending email... Please wait.")
#         QApplication.processEvents()
           
#         try:
#             msg = MIMEMultipart()
#             msg['From'] = sender_email
#             msg['To'] = email_to
#             msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
           
#             body = "Please find attached clinical record data, images, and report documents.\n\n"
#             for k, v in self.selected_patient.items():
#                 if k not in ["image_path", "report_path"]:
#                     body += f"{k.title()}: {v}\n"
                   
#             msg.attach(MIMEText(body, 'plain'))
           
#             img_path = str(self.selected_patient.get("image_path", "")).strip()
#             if img_path and os.path.exists(img_path):
#                 with open(img_path, "rb") as attachment:
#                     part = MIMEBase("application", "octet-stream")
#                     part.set_payload(attachment.read())
#                     encoders.encode_base64(part)
#                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
#                     msg.attach(part)
                   
#             rep_path = str(self.selected_patient.get("report_path", "")).strip()
#             if rep_path and os.path.exists(rep_path):
#                 with open(rep_path, "rb") as attachment:
#                     part = MIMEBase("application", "octet-stream")
#                     part.set_payload(attachment.read())
#                     encoders.encode_base64(part)
#                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
#                     msg.attach(part)
           
#             try:
#                 server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
#                 server.login(sender_email, sender_password)
#                 server.send_message(msg)
#                 server.quit()
#             except Exception:
#                 server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
#                 server.starttls()
#                 server.login(sender_email, sender_password)
#                 server.send_message(msg)
#                 server.quit()
               
#             self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
#             self.status_label.setText("Success: Email sent successfully.")
#         except Exception as e:
#             self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
#             self.status_label.setText(f"Error: {str(e)}")

#     def export_via_bluetooth(self):
#         is_bluetooth_active = False
#         if sys.platform.startswith("linux"):
#             try:
#                 output = subprocess.check_output(["hciconfig"], stderr=subprocess.STDOUT)
#                 if b"UP RUNNING" in output:
#                     is_bluetooth_active = True
#             except Exception:
#                 pass
#         elif sys.platform.startswith("win32"):
#             try:
#                 import winreg
#                 path = r"SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters"
#                 key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
#                 winreg.CloseKey(key)
#                 is_bluetooth_active = True
#             except Exception:
#                 pass
               
#         if not is_bluetooth_active:
#             self.status_label.setText("Error: No Bluetooth device hardware found or turned off.")
#             return
           
#         try:
#             patient_name = self.selected_patient.get('patien_name', 'Patient')
#             data_to_send = f"Patient: {patient_name}\n"
#             for k, v in self.selected_patient.items():
#                 if k not in ["image_path", "report_path"]:
#                     data_to_send += f"{k}: {v}\n"
                   
#             sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
#             nearby_devices = socket.BluetoothSocket(socket.RFCOMM)
#             self.status_label.setText("Scanning for paired RFCOMM Bluetooth devices...")
#         except AttributeError:
#             self.status_label.setText("Error: System Bluetooth Stack / Python RFCOMM sockets unsupported.")
#             return
#         except Exception as e:
#             self.status_label.setText(f"Error: {str(e)}")
#             return
           
#         self.status_label.setText("Error: No matched/paired destination Bluetooth device found.")

#     def export_via_print(self):
#         available_printers = QPrinterInfo.availablePrinters()
#         if not available_printers and not self.check_wifi():
#             self.status_label.setText("Error: No Wi-Fi connection and no local USB printer detected.")
#             return
           
#         printer = QPrinter()
#         dialog = QPrintDialog(printer, self)
#         if dialog.exec() == QPrintDialog.DialogCode.Accepted:
#             self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-weight: bold;")
#             self.status_label.setText("Success: Sent to print queue.")
#         else:
#             self.status_label.setText("Error: No printer device found or printing canceled.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ExportPage()
#     window.showFullScreen()
#     window.show()
#     sys.exit(app.exec())


import sys
import os
import re
import socket
import smtplib
import subprocess
import openpyxl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from keyboard import VirtualKeyboard

orig_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if host == "smtp.gmail.com":
        family = socket.AF_INET
    return orig_getaddrinfo(host, port, family, type, proto, flags)
socket.getaddrinfo = patched_getaddrinfo

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLineEdit, QPushButton, 
                             QComboBox, QScrollArea, QTextBrowser, QRadioButton, QButtonGroup, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo

class ExportPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Export Patient Data")
        self.setFixedSize(1280, 720)
        
        self.data_file = r"data/data.xlsx"
        self.user_file = r"data/user.xlsx"
        self.selected_patient = None
        
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
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(25, 20, 25, 20)
        self.main_layout.setSpacing(15)
        
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
        
        self.content_layout = QHBoxLayout()
        self.main_layout.addLayout(self.content_layout)
        
        self.left_panel = QWidget()
        self.left_panel.setObjectName("LeftPanel")
        self.left_panel.setFixedWidth(390)
        self.left_panel.setStyleSheet("""
            #LeftPanel {
                background-color: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 16px;
            }
        """)
        
        shadow_left = QGraphicsDropShadowEffect(self)
        shadow_left.setBlurRadius(25)
        shadow_left.setColor(QColor(109, 40, 217, 15))
        shadow_left.setOffset(0, 8)
        self.left_panel.setGraphicsEffect(shadow_left)
        
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setSpacing(12)
        self.left_layout.setContentsMargins(25, 25, 25, 25)
        self.content_layout.addWidget(self.left_panel)
        
        self.right_panel = QWidget()
        self.right_panel.setObjectName("RightPanel")
        self.right_panel.setStyleSheet("""
            #RightPanel {
                background-color: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 16px;
            }
        """)
        
        shadow_right = QGraphicsDropShadowEffect(self)
        shadow_right.setBlurRadius(25)
        shadow_right.setColor(QColor(109, 40, 217, 15))
        shadow_right.setOffset(0, 8)
        self.right_panel.setGraphicsEffect(shadow_right)
        
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.addWidget(self.right_panel)
        
        self.setup_left_panel()
        self.setup_right_panel()
        self.keyboard = VirtualKeyboard(self)
        self.keyboard.show()
        self.keyboard.move(100, 480)


    def back_to_dashboard(self):
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "page3.py"])
        self.close()

    def get_doctors_list(self):
        doctors = ["Select Doctor"]
        if os.path.exists(self.user_file):
            try:
                wb = openpyxl.load_workbook(self.user_file, data_only=True)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if len(row) >= 2 and row[1]:
                        doc_name = str(row[1]).strip()
                        if doc_name not in doctors:
                            doctors.append(doc_name)
                wb.close()
            except Exception:
                pass
        return doctors

    def setup_left_panel(self):
        lbl_search_title = QLabel("SEARCH PATIENT DATA")
        lbl_search_title.setStyleSheet("""
            font-family: 'Poppins', 'Inter', sans-serif;
            font-size: 11px;
            font-weight: bold;
            color: #6D28D9; /* Orchid Purple */
            letter-spacing: 2px;
            background: transparent;
        """)
        self.left_layout.addWidget(lbl_search_title)
        
        self.s_name = QLineEdit()
        self.s_name.setPlaceholderText("Patient Name")
        
        self.s_gender = QComboBox()
        self.s_gender.addItems(["Select Gender", "Female"])
        
        self.s_age = QLineEdit()
        self.s_age.setPlaceholderText("Age")
        
        self.s_doctor = QComboBox()
        self.s_doctor.addItems(self.get_doctors_list())
        
        input_style = """
            QLineEdit, QComboBox {
                border: 1px solid rgba(109, 40, 217, 0.18);
                border-radius: 6px;
                padding: 8px 12px;
                background-color: rgba(255, 255, 255, 0.9);
                color: #2E1065; /* Deep Amethyst */
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1.5px solid #6D28D9;
                background-color: #ffffff;
            }
        """
        self.s_name.setStyleSheet(input_style)
        self.s_gender.setStyleSheet(input_style)
        self.s_age.setStyleSheet(input_style)
        self.s_doctor.setStyleSheet(input_style)
        
        self.left_layout.addWidget(self.s_name)
        self.left_layout.addWidget(self.s_gender)
        self.left_layout.addWidget(self.s_age)
        self.left_layout.addWidget(self.s_doctor)
        
        self.btn_search = QPushButton("Search Patient")
        self.btn_search.setMinimumHeight(38)
        self.btn_search.setStyleSheet("""
            QPushButton {
                background-color: #6D28D9; /* Solid Orchid Purple */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        self.btn_search.clicked.connect(self.search_patient)
        self.left_layout.addWidget(self.btn_search)
        
        lbl_export_title = QLabel("EXPORT OPTIONS")
        lbl_export_title.setStyleSheet("""
            font-family: 'Poppins', 'Inter', sans-serif;
            font-size: 11px;
            font-weight: bold;
            color: #6D28D9;
            letter-spacing: 2px;
            background: transparent;
            margin-top: 10px;
        """)
        self.left_layout.addWidget(lbl_export_title)
        
        self.export_group = QButtonGroup(self)
        
        self.rad_email = QRadioButton("Export via Email")
        # self.rad_bluetooth = QRadioButton("Export via Bluetooth")
        self.rad_print = QRadioButton("Print to Printer (USB / Wi-Fi)")
        self.rad_email.setChecked(True)
        
        radio_style = """
            QRadioButton {
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 12px;
                color: #4C1D95; /* Muted Velvet Slate */
                background: transparent;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid rgba(109, 40, 217, 0.3);
                border-radius: 7px;
                background: white;
            }
            QRadioButton::indicator:checked {
                background-color: #EC4899; /* Active Rose */
                border-color: #EC4899;
            }
        """
        self.rad_email.setStyleSheet(radio_style)
        # self.rad_bluetooth.setStyleSheet(radio_style)
        self.rad_print.setStyleSheet(radio_style)
        
        self.export_group.addButton(self.rad_email)
        # self.export_group.addButton(self.rad_bluetooth)
        self.export_group.addButton(self.rad_print)
        
        self.left_layout.addWidget(self.rad_email)
        # self.left_layout.addWidget(self.rad_bluetooth)
        self.left_layout.addWidget(self.rad_print)
        
        self.t_sender_email = QLineEdit()
        self.t_sender_email.setText("oncovuevision@gmail.com")
        self.t_sender_email.setPlaceholderText("Your Gmail Address")
        self.t_sender_email.setStyleSheet(input_style)
        self.left_layout.addWidget(self.t_sender_email)
        
        self.t_sender_pass = QLineEdit()
        self.t_sender_pass.setPlaceholderText("Your App Password (16-character)")
        self.t_sender_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.t_sender_pass.setStyleSheet(input_style)
        self.left_layout.addWidget(self.t_sender_pass)
        
        self.t_email = QLineEdit()
        self.t_email.setPlaceholderText("Recipient Email Address")
        self.t_email.setStyleSheet(input_style)
        self.left_layout.addWidget(self.t_email)
        
        self.btn_export = QPushButton("Export Now")
        self.btn_export.setMinimumHeight(45)
        self.btn_export.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9); /* Rose to Orchid gradient */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F472B6, 
                    stop:1 #7C3AED);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #DB2777, 
                    stop:1 #5B21B6);
            }
        """)
        self.btn_export.clicked.connect(self.execute_export)
        self.left_layout.addWidget(self.btn_export)
        
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("""
            font-family: 'Poppins', sans-serif;
            color: #EF4444; /* Soft Crimson warning accent */
            font-weight: bold;
            font-size: 16px;
            background: transparent;
        """)
        self.left_layout.addWidget(self.status_label)
        self.left_layout.addStretch()

    def setup_right_panel(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(15)
        self.scroll_area.setWidget(self.scroll_content)
        self.right_layout.addWidget(self.scroll_area)
        
        browser_style = """
            QTextBrowser {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 8px;
                padding: 15px;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 13px;
                color: #2E1065; /* Deep Amethyst */
            }
        """
        
        self.info_display = QTextBrowser()
        self.info_display.setPlaceholderText("Patient clinical data will appear here...")
        self.info_display.setFixedHeight(180)
        self.info_display.setStyleSheet(browser_style)
        self.scroll_layout.addWidget(self.info_display)
        
        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setStyleSheet("""
            QLabel {
                border: 2px dashed rgba(109, 40, 217, 0.18);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.4);
                color: #4C1D95;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 12px;
                min-height: 200px;
            }
        """)
        self.scroll_layout.addWidget(self.image_display)
        
        self.report_display = QTextBrowser()
        self.report_display.setPlaceholderText("Report document contents/PDF view...")
        self.report_display.setFixedHeight(180)
        self.report_display.setStyleSheet(browser_style)
        self.scroll_layout.addWidget(self.report_display)

    def search_patient(self):
        self.status_label.clear()
        self.info_display.clear()
        self.image_display.clear()
        self.report_display.clear()
        self.selected_patient = None
        
        name_q = self.s_name.text().strip().lower()
        gender_q = self.s_gender.currentText().strip().lower()
        age_q = self.s_age.text().strip().lower()
        doctor_q = self.s_doctor.currentText().strip().lower()
        
        if not os.path.exists(self.data_file):
            self.status_label.setText("Exception: Patient data file not found.")
            return
            
        found_data = []
        try:
            wb = openpyxl.load_workbook(self.data_file, data_only=True)
            sheet = wb.active
            headers = [str(cell.value).strip().lower() for cell in sheet[1]]
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not any(x is not None for x in row):
                    continue
                row_dict = {headers[i]: row[i] for i in range(len(headers)) if i < len(row)}
                
                p_name = str(row_dict.get("patien_name", "")).strip().lower()
                p_gender = str(row_dict.get("gender", "")).strip().lower()
                p_age = str(row_dict.get("age", "")).strip().lower()
                p_doctor = str(row_dict.get("doctor", "")).strip().lower()
                
                match = True
                if name_q and name_q not in p_name:
                    match = False
                if gender_q != "select gender" and gender_q != p_gender:
                    match = False
                if age_q and age_q != p_age:
                    match = False
                if doctor_q != "select doctor" and doctor_q != p_doctor:
                    match = False
                    
                if match:
                    found_data.append(row_dict)
            wb.close()
        except Exception as e:
            self.status_label.setText(f"Exception: {str(e)}")
            return
            
        if not found_data:
            self.status_label.setText("Exception: No such patient data found.")
            return
            
        self.selected_patient = found_data[0]
        self.display_patient_details(self.selected_patient)

    def display_patient_details(self, data):
        info_text = f"<b>Patient Details</b><br>"
        for k, v in data.items():
            if k not in ["image_path", "report_path"]:
                info_text += f"<b>{k.replace('_', ' ').title()}:</b> {v}<br>"
        self.info_display.setHtml(info_text)
        
        img_path = str(data.get("image_path", "")).strip()
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            scaled_pixmap = pixmap.scaled(500, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_display.setPixmap(scaled_pixmap)
        else:
            self.image_display.setText("Image not available/found at path.")
            
        rep_path = str(data.get("report_path", "")).strip()
        if rep_path and os.path.exists(rep_path):
            if rep_path.endswith(".pdf"):
                self.load_pdf_report(rep_path)
            elif rep_path.endswith(".txt"):
                try:
                    with open(rep_path, "r", encoding="utf-8") as f:
                        self.report_display.setText(f.read())
                except Exception:
                    self.report_display.setText("Error loading report text details.")
            else:
                self.report_display.setText(f"Report path available: {rep_path}\nFile preview restricted inside window.")
        else:
            self.report_display.setText("Report document not available/found at path.")

    def load_pdf_report(self, filepath):
        try:
            import pypdf
            reader = pypdf.PdfReader(filepath)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            if text.strip():
                self.report_display.setText(text)
            else:
                self.report_display.setText("PDF Loaded, but no extractable text content was found.")
        except ImportError:
            self.report_display.setText("To view PDF reports directly, install the required library:\n\npip install pypdf")
        except Exception as e:
            self.report_display.setText(f"Error parsing PDF: {str(e)}")

    def has_internet(self):
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except socket.error:
            return False

    def check_wifi(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            if ip_address.startswith("127."):
                return False
            return True
        except Exception:
            return False

    def validate_email(self, email):
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return bool(re.match(pattern, email))

    def execute_export(self):
        self.status_label.clear()
        if not self.selected_patient:
            self.status_label.setText("Error: Load and select patient details first.")
            return
            
        if self.rad_email.isChecked():
            self.export_via_email()
        # elif self.rad_bluetooth.isChecked():
        #     self.export_via_bluetooth()
        elif self.rad_print.isChecked():
            self.export_via_print()

    # def export_via_email(self):
    #     sender_email = "oncovuevision@gmail.com"
    #     sender_password = "hfix fxjp nvhh diwe"
    #     email_to = self.t_email.text().strip()
        
    #     if not self.validate_email(sender_email):
    #         self.status_label.setText("Error: Invalid sender email address.")
    #         return
            
    #     if not sender_password:
    #         self.status_label.setText("Error: Sender App Password is required.")
    #         return
            
    #     if not self.validate_email(email_to):
    #         self.status_label.setText("Error: Invalid recipient email id.")
    #         return
            
    #     if not self.has_internet():
    #         self.status_label.setText("Error: No internet connection.")
    #         return
            
    #     try:
    #         msg = MIMEMultipart()
    #         msg['From'] = sender_email
    #         msg['To'] = email_to
    #         msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
    #         body = "Please find attached clinical record data, images, and report documents.\n\n"
    #         for k, v in self.selected_patient.items():
    #             if k not in ["image_path", "report_path"]:
    #                 body += f"{k.title()}: {v}\n"
                    
    #         msg.attach(MIMEText(body, 'plain'))
            
    #         img_path = str(self.selected_patient.get("image_path", "")).strip()
    #         if img_path and os.path.exists(img_path):
    #             with open(img_path, "rb") as attachment:
    #                 part = MIMEBase("application", "octet-stream")
    #                 part.set_payload(attachment.read())
    #                 encoders.encode_base64(part)
    #                 part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
    #                 msg.attach(part)
                    
    #         rep_path = str(self.selected_patient.get("report_path", "")).strip()
    #         if rep_path and os.path.exists(rep_path):
    #             with open(rep_path, "rb") as attachment:
    #                 part = MIMEBase("application", "octet-stream")
    #                 part.set_payload(attachment.read())
    #                 encoders.encode_base64(part)
    #                 part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
    #                 msg.attach(part)
            
    #         try:
    #             server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
    #             server.login(sender_email, sender_password)
    #             server.send_message(msg)
    #             server.quit()
    #         except Exception:
    #             server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    #             server.starttls()
    #             server.login(sender_email, sender_password)
    #             server.send_message(msg)
    #             server.quit()
                
    #         self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
    #         self.status_label.setText("Success: Email sent successfully.")
    #     except Exception as e:
    #         self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
    #         self.status_label.setText(f"Error: {str(e)}")

    # def export_via_email(self):
    #     sender_email = "oncovuevision@gmail.com"
    #     sender_password = "hfix fxjp nvhh diwe"
    #     email_to = self.t_email.text().strip()
        
    #     if not self.validate_email(sender_email):
    #         self.status_label.setText("Error: Invalid sender email address.")
    #         return
            
    #     if not sender_password:
    #         self.status_label.setText("Error: Sender App Password is required.")
    #         return
            
    #     if not self.validate_email(email_to):
    #         self.status_label.setText("Error: Invalid recipient email id.")
    #         return
            
    #     if not self.has_internet():
    #         self.status_label.setText("Error: No internet connection detected.")
    #         return
            
    #     # Set temporary status indicating the process has started
    #     self.status_label.setStyleSheet("color: #6D28D9; font-weight: bold;")
    #     self.status_label.setText("Sending email... Please wait.")
    #     QApplication.processEvents()  # Force GUI to refresh and show the message
            
    #     try:
    #         msg = MIMEMultipart()
    #         msg['From'] = sender_email
    #         msg['To'] = email_to
    #         msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
    #         body = "Please find attached clinical record data, images, and report documents.\n\n"
    #         for k, v in self.selected_patient.items():
    #             if k not in ["image_path", "report_path"]:
    #                 body += f"{k.title()}: {v}\n"
                    
    #         msg.attach(MIMEText(body, 'plain'))
            
    #         base_dir = os.path.dirname(os.path.abspath(__file__))
            
    #         img_path = str(self.selected_patient.get("image_path", "")).strip()
    #         if img_path:
    #             if not os.path.isabs(img_path):
    #                 img_path = os.path.join(base_dir, img_path)
    #             if os.path.exists(img_path):
    #                 with open(img_path, "rb") as attachment:
    #                     part = MIMEBase("application", "octet-stream")
    #                     part.set_payload(attachment.read())
    #                     encoders.encode_base64(part)
    #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
    #                     msg.attach(part)
                    
    #         rep_path = str(self.selected_patient.get("report_path", "")).strip()
    #         if rep_path:
    #             if not os.path.isabs(rep_path):
    #                 rep_path = os.path.join(base_dir, rep_path)
    #             if os.path.exists(rep_path):
    #                 with open(rep_path, "rb") as attachment:
    #                     part = MIMEBase("application", "octet-stream")
    #                     part.set_payload(attachment.read())
    #                     encoders.encode_base64(part)
    #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
    #                     msg.attach(part)
            
    #         try:
    #             context = ssl.create_default_context()
    #             server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=12)
    #             server.login(sender_email, sender_password)
    #             server.send_message(msg)
    #             server.quit()
    #         except (ssl.SSLError, ssl.SSLCertVerificationError) as ssl_err:
    #             print(f"[ExportPage] SSL verification failed ({ssl_err}). Retrying with unverified context...")
    #             unverified_context = ssl._create_unverified_context()
    #             server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=unverified_context, timeout=12)
    #             server.login(sender_email, sender_password)
    #             server.send_message(msg)
    #             server.quit()
    #         except Exception:
    #             server = smtplib.SMTP("smtp.gmail.com", 587, timeout=12)
    #             server.starttls()
    #             server.login(sender_email, sender_password)
    #             server.send_message(msg)
    #             server.quit()
                
    #         self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
    #         self.status_label.setText("Success: Email sent successfully.")
    #     except Exception as e:
    #         self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
    #         self.status_label.setText(f"Error details: {str(e)}")

    # def export_via_bluetooth(self):
    #     is_bluetooth_active = False
    #     if sys.platform.startswith("linux"):
    #         try:
    #             output = subprocess.check_output(["hciconfig"], stderr=subprocess.STDOUT)
    #             if b"UP RUNNING" in output:
    #                 is_bluetooth_active = True
    #         except Exception:
    #             pass
    #     elif sys.platform.startswith("win32"):
    #         try:
    #             import winreg
    #             path = r"SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters"
    #             key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    #             winreg.CloseKey(key)
    #             is_bluetooth_active = True
    #         except Exception:
    #             pass
                
    #     if not is_bluetooth_active:
    #         self.status_label.setText("Error: No Bluetooth device hardware found or turned off.")
    #         return
            
    #     try:
    #         patient_name = self.selected_patient.get('patien_name', 'Patient')
    #         data_to_send = f"Patient: {patient_name}\n"
    #         for k, v in self.selected_patient.items():
    #             if k not in ["image_path", "report_path"]:
    #                 data_to_send += f"{k}: {v}\n"
                    
    #         sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    #         nearby_devices = socket.BluetoothSocket(socket.RFCOMM)
    #         self.status_label.setText("Scanning for paired RFCOMM Bluetooth devices...")
    #     except AttributeError:
    #         self.status_label.setText("Error: System Bluetooth Stack / Python RFCOMM sockets unsupported.")
    #         return
    #     except Exception as e:
    #         self.status_label.setText(f"Error: {str(e)}")
    #         return
            
    #     self.status_label.setText("Error: No matched/paired destination Bluetooth device found.")


    # def export_via_email(self):
    #     sender_email = "oncovuevision@gmail.com"
    #     sender_passwords = [
    #         "hfix fxjp nvhh diwe",
    #         "zrqz qkzh xece owls"
    #     ]
    #     email_to = self.t_email.text().strip()
        
    #     if not self.validate_email(sender_email):
    #         self.status_label.setText("Error: Invalid sender email address.")
    #         return
            
    #     if not self.validate_email(email_to):
    #         self.status_label.setText("Error: Invalid recipient email id.")
    #         return
            
    #     logs = []
        
    #     try:
    #         s_net = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #         s_net.settimeout(2)
    #         s_net.connect(("8.8.8.8", 80))
    #         local_ip = s_net.getsockname()[0]
    #         s_net.close()
    #         logs.append(f"[Network] Active interface found. Local IP: {local_ip}")
    #     except Exception as e:
    #         logs.append(f"[Network] Interface check failed: {str(e)}")
            
    #     dns_ok = False
    #     try:
    #         socket.gethostbyname("smtp.gmail.com")
    #         dns_ok = True
    #         logs.append("[DNS] Name resolution to smtp.gmail.com is functional.")
    #     except Exception as e:
    #         logs.append(f"[DNS] Resolution failed. Bypassing standard DNS: {str(e)}")
            

    #     self.status_label.setStyleSheet("color: #6D28D9; font-weight: bold;")
    #     self.status_label.setText("Sending email... Please wait.")
    #     QApplication.processEvents()  # Force GUI to refresh and show the message
            
    #     try:
    #         msg = MIMEMultipart()
    #         msg['From'] = sender_email
    #         msg['To'] = email_to
    #         msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
    #         body = "Please find attached clinical record data, images, and report documents.\n\n"
    #         for k, v in self.selected_patient.items():
    #             if k not in ["image_path", "report_path"]:
    #                 body += f"{k.title()}: {v}\n"
                    
    #         msg.attach(MIMEText(body, 'plain'))
            
    #         base_dir = os.path.dirname(os.path.abspath(__file__))
            
    #         img_path = str(self.selected_patient.get("image_path", "")).strip()
    #         if img_path:
    #             if not os.path.isabs(img_path):
    #                 img_path = os.path.join(base_dir, img_path)
    #             if os.path.exists(img_path):
    #                 with open(img_path, "rb") as attachment:
    #                     part = MIMEBase("application", "octet-stream")
    #                     part.set_payload(attachment.read())
    #                     encoders.encode_base64(part)
    #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
    #                     msg.attach(part)
                    
    #         rep_path = str(self.selected_patient.get("report_path", "")).strip()
    #         if rep_path:
    #             if not os.path.isabs(rep_path):
    #                 rep_path = os.path.join(base_dir, rep_path)
    #             if os.path.exists(rep_path):
    #                 with open(rep_path, "rb") as attachment:
    #                     part = MIMEBase("application", "octet-stream")
    #                     part.set_payload(attachment.read())
    #                     encoders.encode_base64(part)
    #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
    #                     msg.attach(part)
            
    #         smtp_targets = [
    #             "smtp.gmail.com",
    #             "74.125.142.108",
    #             "142.250.115.108",
    #             "173.194.77.108",
    #             "64.233.184.108"
    #         ]
            
    #         connection_established = False
            
    #         for password_idx, password in enumerate(sender_passwords):
    #             logs.append(f"[Auth] Testing Sender App Password Index {password_idx}...")
                
    #             for target in smtp_targets:
    #                 logs.append(f"[SMTP] Attempting connection route -> {target}")
                    
    #                 port_465_open = False
    #                 try:
    #                     s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #                     s_test.settimeout(2)
    #                     s_test.connect((target, 465))
    #                     s_test.close()
    #                     port_465_open = True
    #                     logs.append(f"[Port] Port 465 is reachable on {target}")
    #                 except Exception as e:
    #                     logs.append(f"[Port] Port 465 unreachable on {target}: {str(e)}")
                        
    #                 if port_465_open:
    #                     for attempt in range(1, 4):
    #                         try:
    #                             context = ssl._create_unverified_context()
    #                             server = smtplib.SMTP_SSL(target, 465, context=context, timeout=8)
    #                             server.login(sender_email, password)
    #                             server.send_message(msg)
    #                             server.quit()
    #                             connection_established = True
    #                             logs.append(f"[Success] Email sent via SSL port 465 using target {target}")
    #                             break
    #                         except Exception as e:
    #                             logs.append(f"[Retry] SSL Attempt {attempt} failed on {target}: {str(e)}")
    #                             time.sleep(1)
                                
    #                 if connection_established:
    #                     break
                        
    #                 port_587_open = False
    #                 try:
    #                     s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #                     s_test.settimeout(2)
    #                     s_test.connect((target, 587))
    #                     s_test.close()
    #                     port_587_open = True
    #                     logs.append(f"[Port] Port 587 is reachable on {target}")
    #                 except Exception as e:
    #                     logs.append(f"[Port] Port 587 unreachable on {target}: {str(e)}")
                        
    #                 if port_587_open:
    #                     for attempt in range(1, 4):
    #                         try:
    #                             server = smtplib.SMTP(target, 587, timeout=8)
    #                             server.starttls()
    #                             server.login(sender_email, password)
    #                             server.send_message(msg)
    #                             server.quit()
    #                             connection_established = True
    #                             logs.append(f"[Success] Email sent via TLS port 587 using target {target}")
    #                             break
    #                         except Exception as e:
    #                             logs.append(f"[Retry] TLS Attempt {attempt} failed on {target}: {str(e)}")
    #                             time.sleep(1)
                                
    #                 if connection_established:
    #                     break
                        
    #             if connection_established:
    #                 break
                    
    #         if not connection_established:
    #             formatted_logs = "\n".join(logs[-6:])
    #             raise ConnectionError(f"All SMTP routes failed.\nRecent diagnostic logs:\n{formatted_logs}")
                
    #         self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
    #         self.status_label.setText("Success: Email sent successfully.")
    #     except Exception as e:
    #         self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
    #         self.status_label.setText(f"Error details:\n{str(e)}")


    # def export_via_email(self):
    #     sender_email = "oncovuevision@gmail.com"
    #     sender_passwords = [
    #         "hfix fxjp nvhh diwe",
    #         "zrqz qkzh xece owls"
    #     ]
    #     email_to = self.t_email.text().strip()
       
    #     if not self.validate_email(sender_email):
    #         self.status_label.setText("Error: Invalid sender email address.")
    #         return
           
    #     if not self.validate_email(email_to):
    #         self.status_label.setText("Error: Invalid recipient email id.")
    #         return
           
    #     logs = []
       
    #     try:
    #         s_net = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #         s_net.settimeout(2)
    #         s_net.connect(("8.8.8.8", 80))
    #         local_ip = s_net.getsockname()[0]
    #         s_net.close()
    #         logs.append(f"[Network] Active interface found. Local IP: {local_ip}")
    #     except Exception as e:
    #         logs.append(f"[Network] Interface check failed: {str(e)}")
           
    #     dns_ok = False
    #     try:
    #         socket.gethostbyname("smtp.gmail.com")
    #         dns_ok = True
    #         logs.append("[DNS] Name resolution to smtp.gmail.com is functional.")
    #     except Exception as e:
    #         logs.append(f"[DNS] Resolution failed. Bypassing standard DNS: {str(e)}")
           
    #     try:
    #         msg = MIMEMultipart()
    #         msg['From'] = sender_email
    #         msg['To'] = email_to
    #         msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
           
    #         body = "Please find attached clinical record data, images, and report documents.\n\n"
    #         for k, v in self.selected_patient.items():
    #             if k not in ["image_path", "report_path"]:
    #                 body += f"{k.title()}: {v}\n"
                   
    #         msg.attach(MIMEText(body, 'plain'))
           
    #         base_dir = os.path.dirname(os.path.abspath(__file__))
           
    #         img_path = str(self.selected_patient.get("image_path", "")).strip()
    #         if img_path:
    #             if not os.path.isabs(img_path):
    #                 img_path = os.path.join(base_dir, img_path)
    #             if os.path.exists(img_path):
    #                 with open(img_path, "rb") as attachment:
    #                     part = MIMEBase("application", "octet-stream")
    #                     part.set_payload(attachment.read())
    #                     encoders.encode_base64(part)
    #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
    #                     msg.attach(part)
                   
    #         rep_path = str(self.selected_patient.get("report_path", "")).strip()
    #         if rep_path:
    #             if not os.path.isabs(rep_path):
    #                 rep_path = os.path.join(base_dir, rep_path)
    #             if os.path.exists(rep_path):
    #                 with open(rep_path, "rb") as attachment:
    #                     part = MIMEBase("application", "octet-stream")
    #                     part.set_payload(attachment.read())
    #                     encoders.encode_base64(part)
    #                     part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
    #                     msg.attach(part)
           
    #         smtp_targets = [
    #             "smtp.gmail.com",
    #             "74.125.142.108",
    #             "142.250.115.108",
    #             "173.194.77.108",
    #             "64.233.184.108"
    #         ]
           
    #         connection_established = False
           
    #         for password_idx, password in enumerate(sender_passwords):
    #             logs.append(f"[Auth] Testing Sender App Password Index {password_idx}...")
               
    #             for target in smtp_targets:
    #                 logs.append(f"[SMTP] Attempting connection route -> {target}")
                   
    #                 port_465_open = False
    #                 try:
    #                     s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #                     s_test.settimeout(2)
    #                     s_test.connect((target, 465))
    #                     s_test.close()
    #                     port_465_open = True
    #                     logs.append(f"[Port] Port 465 is reachable on {target}")
    #                 except Exception as e:
    #                     logs.append(f"[Port] Port 465 unreachable on {target}: {str(e)}")
                       
    #                 if port_465_open:
    #                     for attempt in range(1, 4):
    #                         try:
    #                             context = ssl._create_unverified_context()
    #                             server = smtplib.SMTP_SSL(target, 465, context=context, timeout=8)
    #                             server.login(sender_email, password)
    #                             server.send_message(msg)
    #                             server.quit()
    #                             connection_established = True
    #                             logs.append(f"[Success] Email sent via SSL port 465 using target {target}")
    #                             break
    #                         except Exception as e:
    #                             logs.append(f"[Retry] SSL Attempt {attempt} failed on {target}: {str(e)}")
    #                             time.sleep(1)
                               
    #                 if connection_established:
    #                     break
                       
    #                 port_587_open = False
    #                 try:
    #                     s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #                     s_test.settimeout(2)
    #                     s_test.connect((target, 587))
    #                     s_test.close()
    #                     port_587_open = True
    #                     logs.append(f"[Port] Port 587 is reachable on {target}")
    #                 except Exception as e:
    #                     logs.append(f"[Port] Port 587 unreachable on {target}: {str(e)}")
                       
    #                 if port_587_open:
    #                     for attempt in range(1, 4):
    #                         try:
    #                             server = smtplib.SMTP(target, 587, timeout=8)
    #                             server.starttls()
    #                             server.login(sender_email, password)
    #                             server.send_message(msg)
    #                             server.quit()
    #                             connection_established = True
    #                             logs.append(f"[Success] Email sent via TLS port 587 using target {target}")
    #                             break
    #                         except Exception as e:
    #                             logs.append(f"[Retry] TLS Attempt {attempt} failed on {target}: {str(e)}")
    #                             time.sleep(1)
                               
    #                 if connection_established:
    #                     break
                       
    #             if connection_established:
    #                 break
                   
    #         if not connection_established:
    #             formatted_logs = "\n".join(logs[-6:])
    #             raise ConnectionError(f"All SMTP routes failed.\nRecent diagnostic logs:\n{formatted_logs}")
               
    #         self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
    #         self.status_label.setText("Success: Email sent successfully.")
    #     except Exception as e:
    #         error_msg = str(e)
    #         self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
    #         if "10065" in error_msg or "unreachable host" in error_msg.lower():
    #             self.status_label.setText(
    #                 "Error details:\n"
    #                 "Windows Firewall or Antivirus is blocking Python from accessing the internet.\n"
    #                 "To fix, add an Outbound Firewall Exemption in your Antivirus/Windows Defender for:\n"
    #                 f"{sys.executable}"
    #             )
    #         else:
    #             self.status_label.setText(f"Error details:\n{error_msg}")


    def export_via_email(self):
        sender_email = "oncovuevision@gmail.com"
        sender_passwords = [
            "eigw nkdx bfmh ufwy",
            "eigwnkdxbfmhufwy"
        ]
        email_to = self.t_email.text().strip()
        
        if not self.validate_email(sender_email):
            self.status_label.setText("Error: Invalid sender email address.")
            return
            
        if not self.validate_email(email_to):
            self.status_label.setText("Error: Invalid recipient email id.")
            return
            
        logs = []
        
        local_postfix_active = False
        try:
            s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_test.settimeout(1)
            s_test.connect(("127.0.0.1", 25))
            s_test.close()
            local_postfix_active = True
            logs.append("[SMTP] Local Postfix service detected on port 25.")
        except Exception:
            local_postfix_active = False
            logs.append("[SMTP] Local Postfix not detected. Falling back to direct Gmail SMTP.")

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_to
            msg['Subject'] = f"Patient Record Export - {self.selected_patient.get('patien_name', 'Patient')}"
            
            body = "Please find attached clinical record data, images, and report documents.\n\n"
            for k, v in self.selected_patient.items():
                if k not in ["image_path", "report_path"]:
                    body += f"{k.title()}: {v}\n"
                    
            msg.attach(MIMEText(body, 'plain'))
            
            base_dir = os.path.dirname(os.path(__file__))
            
            img_path = str(self.selected_patient.get("image_path", "")).strip()
            if img_path:
                if not os.path.isabs(img_path):
                    img_path = os.path.join(base_dir, img_path)
                if os.path.exists(img_path):
                    with open(img_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(img_path)}")
                        msg.attach(part)
                    
            rep_path = str(self.selected_patient.get("report_path", "")).strip()
            if rep_path:
                if not os.isabs(rep_path):
                    rep_path = os.path.join(base_dir, rep_path)
                if os.path.exists(rep_path):
                    with open(rep_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(rep_path)}")
                        msg.attach(part)
            
            if local_postfix_active:
                try:
                    server = smtplib.SMTP("127.0.0.1", 25, timeout=5)
                    server.send_message(msg)
                    server.quit()
                    self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
                    self.status_label.setText("Success: Email queued locally for delivery.")
                    return
                except Exception as e:
                    logs.append(f"[Fail] Local Postfix dispatch failed: {str(e)}. Falling back to direct Gmail SMTP.")
            
            if not self.has_internet():
                self.status_label.setText("Error: No internet connection detected.")
                return
                
            smtp_targets = [
                "smtp.gmail.com",
                "74.125.142.108",
                "142.250.115.108",
                "173.194.77.108",
                "64.233.184.108"
            ]
            
            connection_established = False
            
            for password_idx, password in enumerate(sender_passwords):
                logs.append(f"[Auth] Testing Sender App Password Index {password_idx}...")
                
                for target in smtp_targets:
                    logs.append(f"[SMTP] Attempting connection route -> {target}")
                    
                    port_465_open = False
                    try:
                        s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s_test.settimeout(2)
                        s_test.connect((target, 465))
                        s_test.close()
                        port_465_open = True
                        logs.append(f"[Port] Port 465 is reachable on {target}")
                    except Exception as e:
                        logs.append(f"[Port] Port 465 unreachable on {target}: {str(e)}")
                        
                    if port_465_open:
                        for attempt in range(1, 4):
                            try:
                                context = ssl._create_unverified_context()
                                server = smtplib.SMTP_SSL(target, 465, context=context, timeout=8)
                                server.login(sender_email, password)
                                server.send_message(msg)
                                server.quit()
                                connection_established = True
                                logs.append(f"[Success] Email sent via SSL port 465 using target {target}")
                                break
                            except Exception as e:
                                logs.append(f"[Retry] SSL Attempt {attempt} failed on {target}: {str(e)}")
                                time.sleep(1)
                                
                    if connection_established:
                        break
                        
                    port_587_open = False
                    try:
                        s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s_test.settimeout(2)
                        s_test.connect((target, 587))
                        s_test.close()
                        port_587_open = True
                        logs.append(f"[Port] Port 587 is reachable on {target}")
                    except Exception as e:
                        logs.append(f"[Port] Port 587 unreachable on {target}: {str(e)}")
                        
                    if port_587_open:
                        for attempt in range(1, 4):
                            try:
                                server = smtplib.SMTP(target, 587, timeout=8)
                                server.starttls()
                                server.login(sender_email, password)
                                server.send_message(msg)
                                server.quit()
                                connection_established = True
                                logs.append(f"[Success] Email sent via TLS port 587 using target {target}")
                                break
                            except Exception as e:
                                logs.append(f"[Retry] TLS Attempt {attempt} failed on {target}: {str(e)}")
                                time.sleep(1)
                                
                    if connection_established:
                        break
                        
                if connection_established:
                    break
                    
            if not connection_established:
                formatted_logs = "\n".join(logs[-6:])
                raise ConnectionError(f"All SMTP routes failed.\nRecent diagnostic logs:\n{formatted_logs}")
                
            self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
            self.status_label.setText("Success: Email sent successfully.")
        except Exception as e:
            error_msg = str(e)
            self.status_label.setStyleSheet("color: #ef4444; font-weight: bold;")
            if "10065" in error_msg or "unreachable host" in error_msg.lower():
                self.status_label.setText(
                    "Error details:\n"
                    "Windows Firewall or Antivirus is blocking Python from accessing the internet.\n"
                    "To fix, add an Outbound Firewall Exemption in your Antivirus/Windows Defender for:\n"
                    f"{sys.executable}"
                )
            else:
                self.status_label.setText(f"Error details:\n{error_msg}")

    def export_via_print(self):
        available_printers = QPrinterInfo.availablePrinters()
        if not available_printers and not self.check_wifi():
            self.status_label.setText("Error: No Wi-Fi connection and no local USB printer detected.")
            return
            
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-weight: bold;")
            self.status_label.setText("Success: Sent to print queue.")
        else:
            self.status_label.setText("Error: No printer device found or printing canceled.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExportPage()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())