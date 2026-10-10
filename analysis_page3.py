
# import sys
# import os
# import subprocess
# import json
# import numpy as np
# from PIL import Image
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
#                              QHBoxLayout, QWidget, QPushButton, QProgressBar, 
#                              QGroupBox, QFileDialog, QGraphicsDropShadowEffect)
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QPixmap, QColor

# try:
#     import tflite_runtime.interpreter as tflite
# except ImportError:
#     try:
#         import tensorflow.lite as tflite
#     except ImportError:
#         pass

# MODEL_PATH = r"model/model.lite"
# LABELS = ["her_0", "her_1", "her_2", "her_3"]

# class AnalysisPage3(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.interpreter = None
#         self.input_details = None
#         self.output_details = None
#         self.selected_image_path = None
#         self.results = {}
        
#         self.setWindowTitle("ncovue - Slide Image Classifier")
#         self.setFixedSize(1280, 720)
        
#         # Central Widget & Background Setup (Soft Pastel Gradient Base)
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
        
#         # Master Vertical Layout
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(25, 20, 25, 20)
#         self.main_layout.setSpacing(15)
        
#         # Top Navigation Bar Layout (Glass Back Button)
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
#         self.btn_back.clicked.connect(self.back_to_previous)
#         self.top_bar.addWidget(self.btn_back)
#         self.top_bar.addStretch()
#         self.main_layout.addLayout(self.top_bar)
        
#         # Split workspace layouts
#         self.body_layout = QHBoxLayout()
#         self.body_layout.setSpacing(15)
#         self.main_layout.addLayout(self.body_layout)
        
#         self.left_panel = QVBoxLayout()
#         self.body_layout.addLayout(self.left_panel, stretch=3)
        
#         self.right_panel = QVBoxLayout()
#         self.body_layout.addLayout(self.right_panel, stretch=2)
        
#         self.setup_left_panel()
#         self.setup_right_panel()
        
#         # Bottom Navigation Controls layout
#         self.bottom_bar = QHBoxLayout()
#         self.btn_proceed = QPushButton("Proceed with Classification Results")
#         self.btn_proceed.setEnabled(False)
#         self.btn_proceed.setMinimumHeight(45)
#         self.btn_proceed.setStyleSheet("""
#             QPushButton {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                     stop:0 #EC4899, 
#                     stop:1 #6D28D9); /* Rose to Orchid gradient */
#                 color: white;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 font-size: 14px;
#                 border: none;
#                 border-radius: 8px;
#             }
#             QPushButton:hover {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                     stop:0 #F472B6, 
#                     stop:1 #7C3AED);
#             }
#             QPushButton:disabled {
#                 background-color: rgba(109, 40, 217, 0.08);
#                 color: rgba(109, 40, 217, 0.35);
#                 border: 1px solid rgba(109, 40, 217, 0.05);
#             }
#         """)
#         self.btn_proceed.clicked.connect(self.save_and_proceed)
#         self.main_layout.addLayout(self.bottom_bar)
#         self.bottom_bar.addWidget(self.btn_proceed)
        
#         self.load_model()
#         self.auto_load_latest_image()

#     def back_to_previous(self):
#         # self.timer.stop()
#         subprocess.Popen([sys.executable, "loader.py"])
#         subprocess.Popen([sys.executable, "analysis_page2.py"])
#         self.close()

#     def setup_left_panel(self):
#         group_style = """
#             QGroupBox {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 11px;
#                 color: #6D28D9; /* Orchid Purple */
#                 font-weight: bold;
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 12px;
#                 margin-top: 10px;
#                 background-color: rgba(255, 255, 255, 0.72);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 12px;
#                 padding: 0 5px;
#             }
#         """
        
#         # Diagnostic Visual container card
#         self.image_group = QGroupBox("Target Diagnostic Frame")
#         self.image_group.setStyleSheet(group_style)
#         img_layout = QVBoxLayout(self.image_group)
#         img_layout.setContentsMargins(15, 20, 15, 15)
#         img_layout.setSpacing(12)
        
#         self.lbl_image = QLabel("No Image Selected")
#         self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.lbl_image.setStyleSheet("""
#             QLabel {
#                 border: 2px dashed rgba(109, 40, 217, 0.18); 
#                 background-color: #000000; 
#                 border-radius: 8px;
#                 color: #C084FC;
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 13px;
#             }
#         """)
#         self.lbl_image.setFixedSize(560, 420)
#         img_layout.addWidget(self.lbl_image)
        
#         self.btn_select = QPushButton("Select Image Manually")
#         self.btn_select.setMinimumHeight(38)
#         self.btn_select.setStyleSheet("""
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
#         self.btn_select.clicked.connect(self.open_image_dialog)
#         img_layout.addWidget(self.btn_select)
        
#         self.left_panel.addWidget(self.image_group)
#         self.left_panel.addStretch()

#         # Apply shadow to target diagnostic card
#         shadow_img = QGraphicsDropShadowEffect(self)
#         shadow_img.setBlurRadius(25)
#         shadow_img.setColor(QColor(109, 40, 217, 15))
#         shadow_img.setOffset(0, 8)
#         self.image_group.setGraphicsEffect(shadow_img)

#     def setup_right_panel(self):
#         group_style = """
#             QGroupBox {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 11px;
#                 color: #6D28D9;
#                 font-weight: bold;
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 12px;
#                 margin-top: 10px;
#                 background-color: rgba(255, 255, 255, 0.72);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 12px;
#                 padding: 0 5px;
#             }
#         """
        
#         # Frosted glass results container card
#         self.results_group = QGroupBox("Classification Results")
#         self.results_group.setStyleSheet(group_style)
#         results_layout = QVBoxLayout(self.results_group)
#         results_layout.setContentsMargins(20, 25, 20, 20)
#         results_layout.setSpacing(10)
        
#         self.class_labels = []
#         self.progress_bars = []
        
#         for i in range(len(LABELS)):
#             lbl = QLabel(f"{LABELS[i].upper().replace('_', ' ')}: 0.0%")
#             lbl.setStyleSheet("""
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 18px; 
#                 color: #4C1D95; /* Velvet Slate */
#                 font-weight: bold;
#             """)
#             results_layout.addWidget(lbl)
#             self.class_labels.append(lbl)
            
#             bar = QProgressBar()
#             bar.setFixedHeight(18)
#             bar.setRange(0, 100)
#             bar.setValue(0)
#             bar.setTextVisible(True)
#             bar.setStyleSheet("""
#                 QProgressBar {
#                     border: none;
#                     background-color: rgba(109, 40, 217, 0.08); /* Frosted lavender track */
#                     color: #2E1065;
#                     text-align: center;
#                     font-family: 'Poppins', sans-serif;
#                     font-weight: bold;
#                     font-size: 10px;
#                     border-radius: 6px;
#                 }
#                 QProgressBar::chunk {
#                     background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                         stop:0 #EC4899, 
#                         stop:1 #C084FC); /* Rose to Lavender gradient chunk */
#                     border-radius: 6px;
#                 }
#             """)
#             results_layout.addWidget(bar)
#             self.progress_bars.append(bar)
            
#         results_layout.addStretch()
        
#         # Clean highlight summary block
#         self.lbl_summary = QLabel("Prediction: None")
#         self.lbl_summary.setStyleSheet("""
#             font-family: 'Poppins', sans-serif;
#             font-size: 20px; 
#             font-weight: bold; 
#             color: #6D28D9; /* Orchid Purple summary font */
#             padding: 10px; 
#             background-color: rgba(109, 40, 217, 0.05); 
#             border: 1px solid rgba(109, 40, 217, 0.15);
#             border-radius: 8px;
#         """)
#         results_layout.addWidget(self.lbl_summary)
        
#         self.right_panel.addWidget(self.results_group)

#         # Apply shadow to the classification result panel
#         shadow_res = QGraphicsDropShadowEffect(self)
#         shadow_res.setBlurRadius(25)
#         shadow_res.setColor(QColor(109, 40, 217, 15))
#         shadow_res.setOffset(0, 8)
#         self.results_group.setGraphicsEffect(shadow_res)

#     def load_model(self):
#         if not os.path.exists(MODEL_PATH):
#             self.lbl_summary.setText("Error: model.lite not found!")
#             return
#         try:
#             self.interpreter = tflite.Interpreter(model_path=MODEL_PATH)
#             self.interpreter.allocate_tensors()
#             self.input_details = self.interpreter.get_input_details()
#             self.output_details = self.interpreter.get_output_details()
#         except Exception as e:
#             self.lbl_summary.setText(f"Error loading model: {str(e)}")

#     def auto_load_latest_image(self):
#         temp_dir = "temp"
#         if os.path.exists(temp_dir):
#             files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#             if files:
#                 latest_image = max(files, key=os.path.getmtime)
#                 self.selected_image_path = latest_image
#                 self.display_image(latest_image)
#                 self.classify_image(latest_image)

#     def open_image_dialog(self):
#         file_path, _ = QFileDialog.getOpenFileName(
#             self, 
#             "Select Image to Classify", 
#             "", 
#             "Images (*.png *.jpg *.jpeg *.bmp)"
#         )
#         if file_path:
#             self.selected_image_path = file_path
#             self.display_image(file_path)
#             self.classify_image(file_path)

#     def display_image(self, file_path):
#         pixmap = QPixmap(file_path)
#         scaled_pixmap = pixmap.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
#         self.lbl_image.setPixmap(scaled_pixmap)

#     def preprocess_image(self, image_path, input_shape):
#         target_height, target_width = input_shape[1], input_shape[2]
#         num_channels = input_shape[3]
        
#         img = Image.open(image_path)
#         if num_channels == 3:
#             img = img.convert('RGB')
#         else:
#             img = img.convert('L')
            
#         img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
#         img_data = np.array(img, dtype=np.float32)
#         img_data = img_data / 255.0
#         img_data = np.expand_dims(img_data, axis=0)
#         return img_data

#     def classify_image(self, image_path):
#         if not self.interpreter:
#             return
            
#         try:
#             input_shape = self.input_details[0]['shape']
#             input_data = self.preprocess_image(image_path, input_shape)
            
#             self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
#             self.interpreter.invoke()
            
#             output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
#             max_idx = np.argmax(output_data)
            
#             for i in range(len(LABELS)):
#                 score = float(output_data[i])
#                 percentage = int(score * 100)
#                 self.class_labels[i].setText(f"{LABELS[i].upper().replace('_', ' ')}: {score*100:.1f}%")
#                 self.progress_bars[i].setValue(percentage)
                
#             predicted_class = LABELS[max_idx]
#             confidence = output_data[max_idx] * 100
            
#             if predicted_class == "her_0":
#                 verdict = "Normal"
#             elif predicted_class == "her_1":
#                 verdict = "Normal"
#             elif predicted_class == "her_2":
#                 verdict = "Equivocal"
#             else:
#                 verdict = "Positive"
                
#             self.lbl_summary.setText(f"Prediction: {verdict.upper()} :: {predicted_class.upper()} : ({confidence:.1f}%)")
            
#             self.results = {
#                 "her0": float(output_data[0]),
#                 "her1": float(output_data[1]),
#                 "her2": float(output_data[2]),
#                 "her3": float(output_data[3]),
#                 "max_class": str(predicted_class).replace("_", ""),
#                 "verdict": verdict
#             }
#             self.btn_proceed.setEnabled(True)
            
#         except Exception as e:
#             self.lbl_summary.setText(f"Error during classification: {str(e)}")

#     def save_and_proceed(self):
#         if not self.results:
#             return
            
#         temp_dir = "temp"
#         os.makedirs(temp_dir, exist_ok=True)
#         filepath = os.path.join(temp_dir, "current_scores.json")
#         try:
#             with open(filepath, "w") as f:
#                 json.dump(self.results, f)
#         except Exception:
#             pass
#         # self.timer.stop()
#         subprocess.Popen([sys.executable, "loader.py"])
#         subprocess.Popen([sys.executable, "analysis_page4.py"])
#         self.close()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = AnalysisPage3()
#     window.showFullScreen()
#     window.show()
#     sys.exit(app.exec())
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import sys
import types
import importlib.util

try:
    import imp
except ImportError:
    imp_mock = types.ModuleType('imp')
    imp_mock.acquire_lock = lambda: None
    imp_mock.release_lock = lambda: None

    def find_module(name, path=None):
        try:
            spec = importlib.util.find_spec(name, path)
            if spec is None:
                raise ImportError(f"No module named {name}")
            return (None, spec.origin or "", ("", "", 0))
        except Exception:
            raise ImportError(f"No module named {name}")

    imp_mock.find_module = find_module
    sys.modules['imp'] = imp_mock

import os
import subprocess
import json
import numpy as np
from PIL import Image
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QProgressBar, 
                             QGroupBox, QFileDialog, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except ImportError:
        tflite = None

MODEL_PATH = r"model/model.lite"
LABELS = ["her_0", "her_1", "her_2", "her_3"]

class AnalysisPage3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.selected_image_path = None
        self.results = {}
        
        self.setWindowTitle("OncoVue - Slide Image Classifier")
        self.setFixedSize(1280, 720)
        
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
        self.btn_back.clicked.connect(self.back_to_previous)
        self.top_bar.addWidget(self.btn_back)
        self.top_bar.addStretch()
        self.main_layout.addLayout(self.top_bar)
        
        self.body_layout = QHBoxLayout()
        self.body_layout.setSpacing(15)
        self.main_layout.addLayout(self.body_layout)
        
        self.left_panel = QVBoxLayout()
        self.body_layout.addLayout(self.left_panel, stretch=3)
        
        self.right_panel = QVBoxLayout()
        self.body_layout.addLayout(self.right_panel, stretch=2)
        
        self.setup_left_panel()
        self.setup_right_panel()
        
        self.bottom_bar = QHBoxLayout()
        self.btn_proceed = QPushButton("Proceed with Classification Results")
        self.btn_proceed.setEnabled(False)
        self.btn_proceed.setMinimumHeight(45)
        self.btn_proceed.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9); /* Rose to Orchid gradient */
                color: white;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F472B6, 
                    stop:1 #7C3AED);
            }
            QPushButton:disabled {
                background-color: rgba(109, 40, 217, 0.08);
                color: rgba(109, 40, 217, 0.35);
                border: 1px solid rgba(109, 40, 217, 0.05);
            }
        """)
        self.btn_proceed.clicked.connect(self.save_and_proceed)
        self.main_layout.addLayout(self.bottom_bar)
        self.bottom_bar.addWidget(self.btn_proceed)
        
        self.load_model()
        self.auto_load_latest_image()

    def back_to_previous(self):
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "analysis_page2.py"])
        self.close()

    def setup_left_panel(self):
        group_style = """
            QGroupBox {
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 11px;
                color: #6D28D9; /* Orchid Purple */
                font-weight: bold;
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 12px;
                margin-top: 10px;
                background-color: rgba(255, 255, 255, 0.72);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }
        """
        
        self.image_group = QGroupBox("Target Diagnostic Frame")
        self.image_group.setStyleSheet(group_style)
        img_layout = QVBoxLayout(self.image_group)
        img_layout.setContentsMargins(15, 20, 15, 15)
        img_layout.setSpacing(12)
        
        self.lbl_image = QLabel("No Image Selected")
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_image.setStyleSheet("""
            QLabel {
                border: 2px dashed rgba(109, 40, 217, 0.18); 
                background-color: #000000; 
                border-radius: 8px;
                color: #C084FC;
                font-family: 'Poppins', sans-serif;
                font-size: 13px;
            }
        """)
        self.lbl_image.setFixedSize(560, 420)
        img_layout.addWidget(self.lbl_image)
        
        self.btn_select = QPushButton("Select Image Manually")
        self.btn_select.setMinimumHeight(38)
        self.btn_select.setStyleSheet("""
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
        self.btn_select.clicked.connect(self.open_image_dialog)
        img_layout.addWidget(self.btn_select)
        
        self.left_panel.addWidget(self.image_group)
        self.left_panel.addStretch()

        shadow_img = QGraphicsDropShadowEffect(self)
        shadow_img.setBlurRadius(25)
        shadow_img.setColor(QColor(109, 40, 217, 15))
        shadow_img.setOffset(0, 8)
        self.image_group.setGraphicsEffect(shadow_img)

    def setup_right_panel(self):
        group_style = """
            QGroupBox {
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 11px;
                color: #6D28D9;
                font-weight: bold;
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 12px;
                margin-top: 10px;
                background-color: rgba(255, 255, 255, 0.72);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }
        """
        
        self.results_group = QGroupBox("Classification Results")
        self.results_group.setStyleSheet(group_style)
        results_layout = QVBoxLayout(self.results_group)
        results_layout.setContentsMargins(20, 25, 20, 20)
        results_layout.setSpacing(10)
        
        self.class_labels = []
        self.progress_bars = []
        
        for i in range(len(LABELS)):
            lbl = QLabel(f"{LABELS[i].upper().replace('_', ' ')}: 0.0%")
            lbl.setStyleSheet("""
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 18px; 
                color: #4C1D95; /* Velvet Slate */
                font-weight: bold;
            """)
            results_layout.addWidget(lbl)
            self.class_labels.append(lbl)
            
            bar = QProgressBar()
            bar.setFixedHeight(18)
            bar.setRange(0, 100)
            bar.setValue(0)
            bar.setTextVisible(True)
            bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    background-color: rgba(109, 40, 217, 0.08); /* Frosted lavender track */
                    color: #2E1065;
                    text-align: center;
                    font-family: 'Poppins', sans-serif;
                    font-weight: bold;
                    font-size: 10px;
                    border-radius: 6px;
                }
                QProgressBar::chunk {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #EC4899, 
                        stop:1 #C084FC); /* Rose to Lavender gradient chunk */
                    border-radius: 6px;
                }
            """)
            results_layout.addWidget(bar)
            self.progress_bars.append(bar)
            
        results_layout.addStretch()
        
        self.lbl_summary = QLabel("Prediction: None")
        self.lbl_summary.setStyleSheet("""
            font-family: 'Poppins', sans-serif;
            font-size: 20px; 
            font-weight: bold; 
            color: #6D28D9; /* Orchid Purple summary font */
            padding: 10px; 
            background-color: rgba(109, 40, 217, 0.05); 
            border: 1px solid rgba(109, 40, 217, 0.15);
            border-radius: 8px;
        """)
        results_layout.addWidget(self.lbl_summary)
        
        self.right_panel.addWidget(self.results_group)

        shadow_res = QGraphicsDropShadowEffect(self)
        shadow_res.setBlurRadius(25)
        shadow_res.setColor(QColor(109, 40, 217, 15))
        shadow_res.setOffset(0, 8)
        self.results_group.setGraphicsEffect(shadow_res)

    def load_model(self):
        if tflite is None:
            self.lbl_summary.setText("Error: tflite-runtime or tensorflow is not installed!")
            return
            
        if not os.path.exists(MODEL_PATH):
            self.lbl_summary.setText("Error: model.lite not found!")
            return
        try:
            self.interpreter = tflite.Interpreter(model_path=MODEL_PATH)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        except Exception as e:
            self.lbl_summary.setText(f"Error loading model: {str(e)}")

    def auto_load_latest_image(self):
        temp_dir = "temp"
        if os.path.exists(temp_dir):
            files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if files:
                latest_image = max(files, key=os.path.getmtime)
                self.selected_image_path = latest_image
                self.display_image(latest_image)
                self.classify_image(latest_image)

    def open_image_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image to Classify", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.selected_image_path = file_path
            self.display_image(file_path)
            self.classify_image(file_path)

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        scaled_pixmap = pixmap.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.lbl_image.setPixmap(scaled_pixmap)

    def preprocess_image(self, image_path, input_shape):
        target_height, target_width = input_shape[1], input_shape[2]
        num_channels = input_shape[3]
        
        img = Image.open(image_path)
        if num_channels == 3:
            img = img.convert('RGB')
        else:
            img = img.convert('L')
            
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        img_data = np.array(img, dtype=np.float32)
        img_data = img_data / 255.0
        img_data = np.expand_dims(img_data, axis=0)
        return img_data

    def classify_image(self, image_path):
        if not self.interpreter:
            return
            
        try:
            input_shape = self.input_details[0]['shape']
            input_data = self.preprocess_image(image_path, input_shape)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            max_idx = np.argmax(output_data)
            
            for i in range(len(LABELS)):
                score = float(output_data[i])
                percentage = int(score * 100)
                self.class_labels[i].setText(f"{LABELS[i].upper().replace('_', ' ')}: {score*100:.1f}%")
                self.progress_bars[i].setValue(percentage)
                
            predicted_class = LABELS[max_idx]
            confidence = output_data[max_idx] * 100
            
            if predicted_class == "her_0":
                verdict = "Normal"
            elif predicted_class == "her_1":
                verdict = "Normal"
            elif predicted_class == "her_2":
                verdict = "Equivocal"
            else:
                verdict = "Positive"
                
            self.lbl_summary.setText(f"Prediction: {verdict.upper()} :: {predicted_class.upper()} : ({confidence:.1f}%)")
            
            self.results = {
                "her0": float(output_data[0]),
                "her1": float(output_data[1]),
                "her2": float(output_data[2]),
                "her3": float(output_data[3]),
                "max_class": str(predicted_class).replace("_", ""),
                "verdict": verdict
            }
            self.btn_proceed.setEnabled(True)
            
        except Exception as e:
            self.lbl_summary.setText(f"Error during classification: {str(e)}")

    def save_and_proceed(self):
        if not self.results:
            return
            
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, "current_scores.json")
        try:
            with open(filepath, "w") as f:
                json.dump(self.results, f)
        except Exception:
            pass
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "analysis_page4.py"])
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnalysisPage3()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())