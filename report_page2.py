import sys
import os
import subprocess
import openpyxl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QGridLayout, QTextBrowser, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor

class ReportDetailWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Patient Clinical Report")
        self.setFixedSize(1280, 720)
        
        self.data_file = r"data/data.xlsx"
        self.phone_arg = sys.argv[1] if len(sys.argv) > 1 else ""
        self.selected_patient = None
        
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
        self.main_layout.setContentsMargins(25, 20, 25, 20)
        self.main_layout.setSpacing(15)
        
        # Top Navigation Bar Layout (Glass Back Button)
        self.top_bar = QHBoxLayout()
        self.btn_back = QPushButton("← Directory")
        self.btn_back.setFixedSize(120, 38)
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
        self.btn_back.clicked.connect(self.back_to_directory)
        self.top_bar.addWidget(self.btn_back)
        self.top_bar.addStretch()
        self.main_layout.addLayout(self.top_bar)
        
        self.load_patient_data()
        
        # Top Metadata Summary Block (Frosted Glass Panel)
        self.top_section = QWidget()
        self.top_section.setObjectName("TopSection")
        self.top_section.setFixedHeight(220)
        self.top_layout = QGridLayout(self.top_section)
        self.top_layout.setContentsMargins(25, 20, 25, 20)
        self.top_layout.setSpacing(12)
        self.top_section.setStyleSheet("""
            #TopSection {
                background-color: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 16px;
            }
        """)
        
        # Apply depth shadow to the metadata summary
        shadow_top = QGraphicsDropShadowEffect(self)
        shadow_top.setBlurRadius(25)
        shadow_top.setColor(QColor(109, 40, 217, 15))
        shadow_top.setOffset(0, 6)
        self.top_section.setGraphicsEffect(shadow_top)
        
        self.main_layout.addWidget(self.top_section)
        
        # Middle Diagnostic Section Layout
        self.middle_section = QHBoxLayout()
        self.middle_section.setSpacing(15)
        self.main_layout.addLayout(self.middle_section)
        
        # Framed Medical Graphics Display Box
        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_display.setStyleSheet("""
            QLabel {
                border: 2px dashed rgba(109, 40, 217, 0.18);
                border-radius: 12px;
                background-color: rgba(255, 255, 255, 0.4);
                color: #4C1D95;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 13px;
            }
        """)
        self.middle_section.addWidget(self.image_display)
        
        # High-Contrast Document Viewer Pane
        self.report_display = QTextBrowser()
        self.report_display.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 12px;
                padding: 15px;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 13px;
                color: #2E1065; /* Deep Amethyst */
            }
        """)
        self.middle_section.addWidget(self.report_display)
        
        # Bottom Export Layout
        self.bottom_section = QHBoxLayout()
        self.btn_export = QPushButton("Export Clinical Report")
        self.btn_export.setMinimumHeight(45)
        self.btn_export.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9); /* Rose to Orchid gradient */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
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
        self.btn_export.clicked.connect(self.open_export_page)
        self.bottom_section.addWidget(self.btn_export)
        self.main_layout.addLayout(self.bottom_section)
        
        self.populate_ui()

    def back_to_directory(self):
                    # self.timer.stop()
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "report_page1.py"])
        self.close()

    def load_patient_data(self):
        if not os.path.exists(self.data_file) or not self.phone_arg:
            return
        try:
            wb = openpyxl.load_workbook(self.data_file, data_only=True)
            sheet = wb.active
            headers = [str(cell.value).strip().lower() for cell in sheet[1]]
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if any(x is not None for x in row):
                    row_dict = {headers[i]: row[i] for i in range(len(headers)) if i < len(row)}
                    if str(row_dict.get("phone_no", "")).strip() == self.phone_arg:
                        self.selected_patient = row_dict
                        break
            wb.close()
        except Exception:
            pass

    def populate_ui(self):
        if not self.selected_patient:
            err_lbl = QLabel("No patient record retrieved or phone argument is missing.")
            err_lbl.setStyleSheet("color: #EF4444; font-weight: bold; font-family: 'Poppins', sans-serif;")
            self.top_layout.addWidget(err_lbl, 0, 0)
            return
            
        data = self.selected_patient
        
        # Accessible text parameters mapped to the palette guidelines
        lbl_style = "font-family: 'Poppins', 'Inter', sans-serif; font-size: 12px; color: #4C1D95; font-weight: 500;"
        val_style = "font-family: 'Poppins', 'Inter', sans-serif; font-size: 13px; font-weight: bold; color: #2E1065;"
        
        details = [
            ("Patient Name", "patien_name"), ("Age", "age"), ("Gender", "gender"),
            ("Phone Number", "phone_no"), ("Doctor Name", "doctor"), ("Hospital", "hospital"),
            ("HER Final", "her_final"), ("Final Prediction", "final_prediction"),
            ("Check Date", "date"), ("Time", "time"), ("HER0", "her0"), ("HER1", "her1"),
            ("HER2", "her2"), ("HER3", "her3"), ("HER Final Value", "her_final")
        ]
        
        row_idx, col_idx = 0, 0
        for label, key in details:
            lbl = QLabel(f"{label}:")
            lbl.setStyleSheet(lbl_style)
            val = QLabel(str(data.get(key, "")))
            val.setStyleSheet(val_style)
            
            self.top_layout.addWidget(lbl, row_idx, col_idx * 2)
            self.top_layout.addWidget(val, row_idx, col_idx * 2 + 1)
            
            col_idx += 1
            if col_idx > 2:
                col_idx = 0
                row_idx += 1
                
        img_path = str(data.get("image_path", "")).strip()
        if img_path and os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            self.image_display.setPixmap(pixmap.scaled(480, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_display.setText("Patient image not found/available.")
            
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
                self.report_display.setText(f"File: {rep_path}\nLocal preview restricted inside panel.")
        else:
            self.report_display.setText("Patient report document not found/available.")

    def load_pdf_report(self, filepath):
        try:
            import pypdf
            reader = pypdf.PdfReader(filepath)
            
            # Incorporate premium design tokens inline with the extracted HTML structure
            html_content = "<div style='font-family: Poppins, Inter, sans-serif; line-height: 1.6; color: #2e1065; padding: 5px;'>"
            
            for idx, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    formatted_text = extracted.replace("\n", "<br>")
                    html_content += f"<div style='background-color: rgba(255, 255, 255, 0.95); padding: 25px; margin-bottom: 20px; border: 1px solid rgba(109, 40, 217, 0.12); border-radius: 8px; box-shadow: 0 4px 12px rgba(109, 40, 217, 0.03);'>"
                    html_content += f"<p style='text-align: right; font-size: 11px; color: #c084fc; border-bottom: 1px solid rgba(109, 40, 217, 0.1); padding-bottom: 5px; margin-bottom: 15px;'>Page {idx+1} of {len(reader.pages)}</p>"
                    html_content += f"<div style='font-size: 13px; font-weight: normal; color: #2e1065;'>{formatted_text}</div>"
                    html_content += "</div>"
                    
            html_content += "</div>"
            
            if len(reader.pages) > 0:
                self.report_display.setHtml(html_content)
            else:
                self.report_display.setPlainText("PDF Loaded, but no extractable text content was found.")
        except ImportError:
            self.report_display.setPlainText("To view PDF reports directly, install the required library:\n\npip install pypdf")
        except Exception as e:
            self.report_display.setPlainText(f"Error parsing PDF: {str(e)}")

    def open_export_page(self):
        if self.selected_patient:
            phone_no = str(self.selected_patient.get("phone_no", ""))
                    # self.timer.stop()
            subprocess.Popen([sys.executable, "loader.py"])
            subprocess.Popen([sys.executable, "report_export_page.py", phone_no])
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportDetailWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())