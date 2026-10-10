# import sys
# import os
# import subprocess
# import time
# import numpy as np
# import cv2
# import serial
# import serial.tools.list_ports

# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
#     QGroupBox, QComboBox, QPushButton, QLabel, QSpinBox, QSlider,
#     QMessageBox, QGraphicsDropShadowEffect
# )
# from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
# from PyQt6.QtGui import QImage, QPixmap, QColor


# class CameraThread(QThread):
#     # Emits the enhanced GUI-display QImage and the pristine zoomed BGR frame for saving
#     change_pixmap_signal = pyqtSignal(QImage, object)

#     def __init__(self):
#         super().__init__()
#         self._run_flag = True
#         self.zoom_factor = 1.0  # Controls the dynamic ROI crop size

#     def set_zoom(self, zoom_val):
#         self.zoom_factor = float(zoom_val)

#     def run(self):
#         # 1. Raspberry Pi Picamera2 stack
#         try:
#             from picamera2 import Picamera2
#             picam = Picamera2()
#             config = picam.create_preview_configuration(
#                 main={"size": (4056, 3040), "format": "RGB888"}
#             )
#             picam.configure(config)
#             picam.start()
            
#             # Discard initial frames to let the sensor's Auto Exposure/White Balance settle
#             self.msleep(600)
            
#             while self._run_flag:
#                 frame = picam.capture_array() 
#                 if frame is not None:
#                     # Convert incoming BGR frame to RGB
#                     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                     h, w, ch = frame.shape
                    
#                     # Centered base crop setup
#                     base_crop_size = min(2500, h, w)
                    
#                     # Apply Digital Zoom by reducing the size of the sensor crop window
#                     zoom_size = int(base_crop_size / self.zoom_factor)
#                     zoom_size = max(200, min(zoom_size, base_crop_size))  # Prevent division bounds issues
                    
#                     start_y = (h - zoom_size) // 2
#                     start_x = (w - zoom_size) // 2
                    
#                     # Crop raw frame at the active zoom level and force contiguous memory layout
#                     cropped_rgb = np.ascontiguousarray(
#                         frame[start_y:start_y+zoom_size, start_x:start_x+zoom_size]
#                     )
#                     cropped_bgr = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2BGR)
                    
#                     # --- PREVIEW PIPELINE ---
#                     # Downsample the zoomed slice to stream standard display dimensions
#                     preview_size = 800
#                     preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
#                     # Dynamic Illumination Boost (CLAHE in LAB color space)
#                     lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
#                     l, a, b = cv2.split(lab)
#                     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#                     cl = clahe.apply(l)
#                     enhanced_lab = cv2.merge((cl, a, b))
#                     preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
#                     # Gentle Sharpening
#                     sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
#                     preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
#                     preview_rgb = np.ascontiguousarray(preview_rgb)
#                     bytes_per_line = preview_rgb.strides[0]
                    
#                     q_image = QImage(
#                         preview_rgb.data, preview_size, preview_size, bytes_per_line, QImage.Format.Format_RGB888
#                     ).copy()
                    
#                     self.change_pixmap_signal.emit(q_image, cropped_bgr)
#                 self.msleep(33)
                
#             picam.stop()
#             picam.close()

#         # 2. Fallback OpenCV VideoCapture
#         except ImportError:
#             cap = cv2.VideoCapture(0)
#             cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
#             cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4056)
#             cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3040)
            
#             # Warmup sequence
#             for _ in range(15):
#                 cap.read()
            
#             while self._run_flag:
#                 ret, frame = cap.read()
#                 if ret:
#                     h, w, ch = frame.shape
                    
#                     base_crop_size = min(2500, h, w)
                    
#                     # Apply Digital Zoom by reducing the size of the sensor crop window
#                     zoom_size = int(base_crop_size / self.zoom_factor)
#                     zoom_size = max(200, min(zoom_size, base_crop_size))
                    
#                     start_y = (h - zoom_size) // 2
#                     start_x = (w - zoom_size) // 2
                    
#                     cropped_bgr = np.ascontiguousarray(
#                         frame[start_y:start_y+zoom_size, start_x:start_x+zoom_size]
#                     )
#                     cropped_rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)
                    
#                     # --- PREVIEW PIPELINE ---
#                     preview_size = 800
#                     preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
#                     # Dynamic Illumination Boost
#                     lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
#                     l, a, b = cv2.split(lab)
#                     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#                     cl = clahe.apply(l)
#                     enhanced_lab = cv2.merge((cl, a, b))
#                     preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
#                     # Gentle Sharpening
#                     sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
#                     preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
#                     preview_rgb = np.ascontiguousarray(preview_rgb)
#                     bytes_per_line = preview_rgb.strides[0]
                    
#                     q_image = QImage(
#                         preview_rgb.data, preview_size, preview_size, bytes_per_line, QImage.Format.Format_RGB888
#                     ).copy()
                    
#                     self.change_pixmap_signal.emit(q_image, cropped_bgr)
#                 else:
#                     self.change_pixmap_signal.emit(QImage(), None)
#                 self.msleep(33)
#             cap.release()

#     def stop(self):
#         self._run_flag = False
#         self.wait()


# class MainAppWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ser = None
#         self.current_frame = None
#         self.last_captured_path = None
        
#         self.setWindowTitle("OncoVue - Control & Analysis Interface")
#         self.setFixedSize(1280, 720)
        
#         # Central Widget & Soft Gradient Background
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
        
#         # Layout Config
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(15, 10, 15, 10)
#         self.main_layout.setSpacing(10)
        
#         # Top Action Bar
#         self.top_bar = QHBoxLayout()
#         self.btn_back = QPushButton("← Back")
#         self.btn_back.setFixedSize(100, 32)
#         self.btn_back.setStyleSheet("""
#             QPushButton {
#                 background-color: rgba(109, 40, 217, 0.08);
#                 border: 1px solid rgba(109, 40, 217, 0.18);
#                 color: #4C1D95;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 border-radius: 6px;
#                 font-size: 12px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(109, 40, 217, 0.15);
#                 border-color: rgba(109, 40, 217, 0.3);
#             }
#         """)
#         self.btn_back.clicked.connect(self.back_to_dashboard)
#         self.top_bar.addWidget(self.btn_back)
#         self.top_bar.addStretch()
#         self.main_layout.addLayout(self.top_bar)
        
#         # Grid/Columns
#         self.content_layout = QHBoxLayout()
#         self.content_layout.setSpacing(15)
#         self.main_layout.addLayout(self.content_layout)
        
#         self.left_panel = QVBoxLayout()
#         self.left_panel.setSpacing(10)
#         self.content_layout.addLayout(self.left_panel, stretch=1)
        
#         self.right_panel = QVBoxLayout()
#         self.right_panel.setSpacing(10)
#         self.content_layout.addLayout(self.right_panel, stretch=3)
        
#         # Setup Widgets
#         self.setup_left_panel()
#         self.setup_right_panel()
        
#         # Serial Read Timers
#         self.serial_timer = QTimer()
#         self.serial_timer.timeout.connect(self.read_serial_data)

#         # Start Capture Thread
#         self.camera_thread = CameraThread()
#         self.camera_thread.change_pixmap_signal.connect(self.update_frame)
#         self.camera_thread.start()

#     def setup_left_panel(self):
#         group_style = """
#             QGroupBox {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 11px;
#                 color: #6D28D9;
#                 font-weight: bold;
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 10px;
#                 margin-top: 8px;
#                 background-color: rgba(255, 255, 255, 0.72);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 10px;
#                 padding: 0 4px;
#             }
#             QLabel {
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 11px;
#                 color: #4C1D95;
#                 font-weight: 500;
#             }
#         """
        
#         input_style = """
#             QComboBox, QSpinBox {
#                 border: 1px solid rgba(109, 40, 217, 0.18);
#                 border-radius: 5px;
#                 padding: 4px 8px;
#                 background-color: rgba(255, 255, 255, 0.9);
#                 color: #2E1065;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 11px;
#             }
#             QComboBox:focus, QSpinBox:focus {
#                 border: 1.2px solid #6D28D9;
#                 background-color: #ffffff;
#             }
#         """
        
#         btn_style = """
#             QPushButton {
#                 background-color: rgba(192, 132, 252, 0.12);
#                 border: 1px solid rgba(192, 132, 252, 0.25);
#                 color: #4C1D95;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 border-radius: 5px;
#                 padding: 6px;
#                 font-size: 11px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(192, 132, 252, 0.22);
#                 border-color: rgba(192, 132, 252, 0.4);
#             }
#             QPushButton:disabled {
#                 background-color: rgba(255, 255, 255, 0.3);
#                 border-color: rgba(109, 40, 217, 0.08);
#                 color: #C084FC;
#             }
#         """

#         # 1. Serial Connection
#         self.conn_group = QGroupBox("Serial Connection")
#         self.conn_group.setStyleSheet(group_style)
#         conn_layout = QHBoxLayout(self.conn_group)
#         conn_layout.setContentsMargins(10, 16, 10, 10)
        
#         self.port_combo = QComboBox()
#         self.port_combo.setStyleSheet(input_style)
#         self.refresh_ports()
#         conn_layout.addWidget(self.port_combo)
        
#         self.refresh_btn = QPushButton("Refresh")
#         self.refresh_btn.setStyleSheet(btn_style)
#         self.refresh_btn.clicked.connect(self.refresh_ports)
#         conn_layout.addWidget(self.refresh_btn)
        
#         self.connect_btn = QPushButton("Connect")
#         self.connect_btn.setStyleSheet(btn_style + "QPushButton{background-color: #10B981; color: white; border: none;} QPushButton:hover{background-color: #059669;}")
#         self.connect_btn.clicked.connect(self.toggle_connection)
#         conn_layout.addWidget(self.connect_btn)
#         self.left_panel.addWidget(self.conn_group)

#         # 2. X-Axis Controls
#         self.s1_group = QGroupBox("X-Axis Controls (Left/Right)")
#         self.s1_group.setStyleSheet(group_style)
#         s1_layout = QVBoxLayout(self.s1_group)
#         s1_layout.setContentsMargins(10, 16, 10, 10)
#         s1_layout.setSpacing(6)
        
#         step_lay1 = QHBoxLayout()
#         step_lay1.addWidget(QLabel("Step Size:"))
#         self.s1_step = QSpinBox()
#         self.s1_step.setStyleSheet(input_style)
#         self.s1_step.setRange(1, 1800)
#         self.s1_step.setValue(90)
#         step_lay1.addWidget(self.s1_step)
#         s1_layout.addLayout(step_lay1)
        
#         btn_lay1 = QHBoxLayout()
#         self.s1_left_btn = QPushButton("- Custom")
#         self.s1_left_btn.setStyleSheet(btn_style)
#         self.s1_left_btn.clicked.connect(lambda: self.send_servo_command("s1", "left", self.s1_step.value()))
#         self.s1_right_btn = QPushButton("+ Custom")
#         self.s1_right_btn.setStyleSheet(btn_style)
#         self.s1_right_btn.clicked.connect(lambda: self.send_servo_command("s1", "right", self.s1_step.value()))
#         btn_lay1.addWidget(self.s1_left_btn)
#         btn_lay1.addWidget(self.s1_right_btn)
#         s1_layout.addLayout(btn_lay1)

#         fast_lay1 = QHBoxLayout()
#         self.s1_m20 = QPushButton("- 20°")
#         self.s1_m20.setStyleSheet(btn_style)
#         self.s1_m20.clicked.connect(lambda: self.send_servo_command("s1", "left", 20))
#         self.s1_p20 = QPushButton("+ 20°")
#         self.s1_p20.setStyleSheet(btn_style)
#         self.s1_p20.clicked.connect(lambda: self.send_servo_command("s1", "right", 20))
#         fast_lay1.addWidget(self.s1_m20)
#         fast_lay1.addWidget(self.s1_p20)
#         s1_layout.addLayout(fast_lay1)
#         self.left_panel.addWidget(self.s1_group)

#         # 3. Y-Axis Controls
#         self.s2_group = QGroupBox("Y-Axis Controls (Up/Down)")
#         self.s2_group.setStyleSheet(group_style)
#         s2_layout = QVBoxLayout(self.s2_group)
#         s2_layout.setContentsMargins(10, 16, 10, 10)
#         s2_layout.setSpacing(6)
        
#         step_lay2 = QHBoxLayout()
#         step_lay2.addWidget(QLabel("Step Size:"))
#         self.s2_step = QSpinBox()
#         self.s2_step.setStyleSheet(input_style)
#         self.s2_step.setRange(1, 1800)
#         self.s2_step.setValue(90)
#         step_lay2.addWidget(self.s2_step)
#         s2_layout.addLayout(step_lay2)
        
#         btn_lay2 = QHBoxLayout()
#         self.s2_left_btn = QPushButton("- Custom")
#         self.s2_left_btn.setStyleSheet(btn_style)
#         self.s2_left_btn.clicked.connect(lambda: self.send_servo_command("s2", "left", self.s2_step.value()))
#         self.s2_right_btn = QPushButton("+ Custom")
#         self.s2_right_btn.setStyleSheet(btn_style)
#         self.s2_right_btn.clicked.connect(lambda: self.send_servo_command("s2", "right", self.s2_step.value()))
#         btn_lay2.addWidget(self.s2_left_btn)
#         btn_lay2.addWidget(self.s2_right_btn)
#         s2_layout.addLayout(btn_lay2)

#         fast_lay2 = QHBoxLayout()
#         self.s2_m20 = QPushButton("- 20°")
#         self.s2_m20.setStyleSheet(btn_style)
#         self.s2_m20.clicked.connect(lambda: self.send_servo_command("s2", "left", 20))
#         self.s2_p20 = QPushButton("+ 20°")
#         self.s2_p20.setStyleSheet(btn_style)
#         self.s2_p20.clicked.connect(lambda: self.send_servo_command("s2", "right", 20))
#         fast_lay2.addWidget(self.s2_m20)
#         fast_lay2.addWidget(self.s2_p20)
#         s2_layout.addLayout(fast_lay2)
#         self.left_panel.addWidget(self.s2_group)

#         # 4. Zoom Control
#         self.zoom_group = QGroupBox("Lossless Digital Zoom")
#         self.zoom_group.setStyleSheet(group_style)
#         zoom_layout = QVBoxLayout(self.zoom_group)
#         zoom_layout.setContentsMargins(10, 16, 10, 10)
#         zoom_layout.setSpacing(6)
        
#         zoom_info_layout = QHBoxLayout()
#         self.zoom_label = QLabel("Zoom Factor: 1.0x")
#         zoom_info_layout.addWidget(self.zoom_label)
#         zoom_info_layout.addStretch()
#         zoom_layout.addLayout(zoom_info_layout)
        
#         self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
#         self.zoom_slider.setMinimum(10)  # Representing 1.0x
#         self.zoom_slider.setMaximum(40)  # Representing 4.0x
#         self.zoom_slider.setValue(10)
#         self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
#         self.zoom_slider.setTickInterval(5)
#         self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
#         zoom_layout.addWidget(self.zoom_slider)
#         self.left_panel.addWidget(self.zoom_group)

#         # 5. Capture & File Action Panel
#         self.action_group = QGroupBox("Capture & Analysis Pipeline")
#         self.action_group.setStyleSheet(group_style)
#         action_layout = QVBoxLayout(self.action_group)
#         action_layout.setContentsMargins(10, 16, 10, 10)
#         action_layout.setSpacing(8)
        
#         btn_action_style = """
#             QPushButton {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 font-size: 11px;
#                 border: none;
#                 border-radius: 5px;
#                 padding: 8px 12px;
#                 color: white;
#             }
#             QPushButton:disabled {
#                 background-color: rgba(109, 40, 217, 0.08);
#                 color: rgba(109, 40, 217, 0.35);
#                 border: 1px solid rgba(109, 40, 217, 0.05);
#             }
#         """
        
#         self.btn_capture = QPushButton("Capture Image")
#         self.btn_capture.setStyleSheet(btn_action_style + """
#             QPushButton { background-color: #6D28D9; }
#             QPushButton:hover { background-color: #7C3AED; }
#             QPushButton:pressed { background-color: #5B21B6; }
#         """)
#         self.btn_capture.clicked.connect(self.capture_image)
#         action_layout.addWidget(self.btn_capture)
        
#         self.btn_discard = QPushButton("Discard Capture")
#         self.btn_discard.setEnabled(False)
#         self.btn_discard.setStyleSheet(btn_action_style + """
#             QPushButton { background-color: #EF4444; }
#             QPushButton:hover { background-color: #DC2626; }
#             QPushButton:pressed { background-color: #B91C1C; }
#         """)
#         self.btn_discard.clicked.connect(self.discard_image)
#         action_layout.addWidget(self.btn_discard)
        
#         self.btn_proceed = QPushButton("Proceed to Diagnostics")
#         self.btn_proceed.setEnabled(False)
#         self.btn_proceed.setStyleSheet(btn_action_style + """
#             QPushButton {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                     stop:0 #EC4899, 
#                     stop:1 #6D28D9);
#             }
#             QPushButton:hover {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                     stop:0 #F472B6, 
#                     stop:1 #7C3AED);
#             }
#         """)
#         self.btn_proceed.clicked.connect(self.proceed_next)
#         action_layout.addWidget(self.btn_proceed)
        
#         self.left_panel.addWidget(self.action_group)
        
#         self.left_panel.addStretch()
#         self.set_controls_enabled(False)

#     def setup_right_panel(self):
#         group_style = """
#             QGroupBox {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 11px;
#                 color: #6D28D9;
#                 font-weight: bold;
#                 border: 1px solid rgba(109, 40, 217, 0.15);
#                 border-radius: 12px;
#                 margin-top: 8px;
#                 background-color: rgba(255, 255, 255, 0.72);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 12px;
#                 padding: 0 4px;
#             }
#         """
        
#         # Stream Viewport Area
#         self.cam_group = QGroupBox("Diagnostic Viewport")
#         self.cam_group.setStyleSheet(group_style)
#         cam_layout = QVBoxLayout(self.cam_group)
#         cam_layout.setContentsMargins(10, 15, 10, 10)
        
#         self.camera_label = QLabel("Loading Camera Stream...")
#         self.camera_label.setFixedSize(900, 530)
#         self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.camera_label.setStyleSheet("""
#             QLabel {
#                 border: 2px dashed rgba(109, 40, 217, 0.2); 
#                 background-color: #000000; 
#                 border-radius: 12px;
#                 color: #C084FC;
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 13px;
#             }
#         """)
        
#         # Viewport Drop Shadow
#         shadow_cam = QGraphicsDropShadowEffect(self)
#         shadow_cam.setBlurRadius(25)
#         shadow_cam.setColor(QColor(109, 40, 217, 20))
#         shadow_cam.setOffset(0, 5)
#         self.camera_label.setGraphicsEffect(shadow_cam)
#         cam_layout.addWidget(self.camera_label, alignment=Qt.AlignmentFlag.AlignCenter)
#         self.right_panel.addWidget(self.cam_group)

#         # Operational Status Message Line
#         self.status_label = QLabel("")
#         self.status_label.setStyleSheet("""
#             font-family: 'Poppins', sans-serif;
#             color: #10B981;
#             font-size: 12px; 
#             font-weight: bold;
#             background: transparent;
#         """)
#         self.right_panel.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

#     def on_zoom_changed(self, val):
#         zoom_factor = val / 10.0
#         self.zoom_label.setText(f"Zoom Factor: {zoom_factor:.1f}x")
#         self.camera_thread.set_zoom(zoom_factor)

#     def back_to_dashboard(self):
#         self.camera_thread.stop()
#         self.close_serial()
#         subprocess.Popen([sys.executable, "analysis_page1.py"])
#         self.close()

#     def proceed_next(self):
#         self.camera_thread.stop()
#         self.close_serial()
#         subprocess.Popen([sys.executable, "analysis_page3.py"])
#         self.close()

#     def update_frame(self, q_image, cropped_bgr):
#         if cropped_bgr is not None and not q_image.isNull():
#             self.current_frame = cropped_bgr
#             pixmap = QPixmap.fromImage(q_image).scaled(
#                 900, 530, 
#                 Qt.AspectRatioMode.KeepAspectRatio, 
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self.camera_label.setPixmap(pixmap)
#             self.camera_label.setStyleSheet("""
#                 QLabel {
#                     border: 2px dashed rgba(109, 40, 217, 0.2); 
#                     background-color: #000000; 
#                     border-radius: 12px;
#                 }
#             """)
#         else:
#             self.camera_label.setPixmap(QPixmap())
#             self.camera_label.setText("No camera device found/accessible.")
#             self.camera_label.setStyleSheet("""
#                 color: #EF4444; 
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 14px; 
#                 font-weight: bold; 
#                 border: 2px dashed rgba(239, 68, 68, 0.3); 
#                 background-color: #000000; 
#                 border-radius: 12px;
#             """)

#     def capture_image(self):
#         self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#         self.status_label.clear()
        
#         if self.current_frame is None:
#             self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#             self.status_label.setText("Error: No live frame to capture.")
#             return
            
#         temp_dir = "temp"
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
            
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         zoom_suffix = f"_{int(self.camera_thread.zoom_factor * 10)}z"
#         filename = f"captured_{timestamp}{zoom_suffix}.png"
#         filepath = os.path.join(temp_dir, filename)
        
#         try:
#             # Writes the high-res frame corresponding to the active zoom crop
#             cv2.imwrite(filepath, self.current_frame)
#             self.last_captured_path = filepath
#             self.btn_discard.setEnabled(True)
#             self.btn_proceed.setEnabled(True)
#             self.status_label.setText(f"Success: Zoomed frame saved to {filepath}")
#         except Exception as e:
#             self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#             self.status_label.setText(f"Error saving image: {str(e)}")

#     def discard_image(self):
#         self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#         self.status_label.clear()
        
#         if self.last_captured_path and os.path.exists(self.last_captured_path):
#             try:
#                 os.remove(self.last_captured_path)
#                 self.status_label.setText(f"Discarded: {self.last_captured_path} deleted successfully.")
#                 self.last_captured_path = None
#                 self.btn_discard.setEnabled(False)
#                 self.btn_proceed.setEnabled(False)
#             except Exception as e:
#                 self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#                 self.status_label.setText(f"Error discarding file: {str(e)}")
#         else:
#             self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#             self.status_label.setText("Error: No active image found to discard.")

#     # --- SERIAL HARDWARE COMMUNICATIONS ---
#     def refresh_ports(self):
#         self.port_combo.clear()
#         ports = list(serial.tools.list_ports.comports())
#         for port in ports:
#             self.port_combo.addItem(port.device)

#     def toggle_connection(self):
#         if self.ser is None:
#             port = self.port_combo.currentText()
#             if not port:
#                 QMessageBox.warning(self, "Warning", "Select serial port first.")
#                 return
#             try:
#                 self.ser = serial.Serial(port, 9600, timeout=0.1)
#                 time.sleep(2)  # Delay for hardware power transition
#                 self.ser.reset_input_buffer()
                
#                 self.connect_btn.setText("Disconnect")
#                 self.connect_btn.setStyleSheet("""
#                     QPushButton {
#                         background-color: #EF4444; 
#                         color: white; 
#                         font-family: 'Poppins', sans-serif;
#                         font-weight: bold; 
#                         border: none;
#                         border-radius: 5px; 
#                         padding: 6px;
#                     }
#                     QPushButton:hover {
#                         background-color: #DC2626;
#                     }
#                 """)
#                 self.set_controls_enabled(True)
#                 self.serial_timer.start(50)
#                 self.status_label.setText(f"Serial connection opened: {port}")
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"Failed to open port: {e}")
#                 self.ser = None
#         else:
#             self.close_serial()
#             self.connect_btn.setText("Connect")
#             self.connect_btn.setStyleSheet("""
#                 QPushButton {
#                     background-color: #10B981; 
#                     color: white; 
#                     font-family: 'Poppins', sans-serif;
#                     font-weight: bold; 
#                     border: none;
#                     border-radius: 5px; 
#                     padding: 6px;
#                 }
#                 QPushButton:hover {
#                     background-color: #059669;
#                 }
#             """)
#             self.set_controls_enabled(False)
#             self.status_label.setText("Serial connection closed.")

#     def close_serial(self):
#         self.serial_timer.stop()
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.close()
#             except Exception:
#                 pass
#         self.ser = None

#     def set_controls_enabled(self, enabled):
#         self.s1_left_btn.setEnabled(enabled)
#         self.s1_right_btn.setEnabled(enabled)
#         self.s1_m20.setEnabled(enabled)
#         self.s1_p20.setEnabled(enabled)
#         self.s2_left_btn.setEnabled(enabled)
#         self.s2_right_btn.setEnabled(enabled)
#         self.s2_m20.setEnabled(enabled)
#         self.s2_p20.setEnabled(enabled)

#     def send_servo_command(self, servo_id, direction, degrees):
#         command = f"{servo_id} {direction} {degrees}\n"
#         self.write_to_serial(command)

#     def write_to_serial(self, command):
#         if self.ser and self.ser.is_open:
#             try:
#                 self.ser.write(command.encode('utf-8'))
#             except Exception as e:
#                 self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#                 self.status_label.setText(f"Serial write fail: {str(e)}")
#                 self.toggle_connection()

#     def read_serial_data(self):
#         if self.ser and self.ser.is_open:
#             try:
#                 while self.ser.in_waiting > 0:
#                     line = self.ser.readline().decode('utf-8').strip()
#                     if line:
#                         self.status_label.setText(f"Hardware response: {line}")
#             except Exception as e:
#                 self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: bold;")
#                 self.status_label.setText(f"Serial read fail: {str(e)}")
#                 self.toggle_connection()

#     def closeEvent(self, event):
#         self.camera_thread.stop()
#         self.close_serial()
#         event.accept()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainAppWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
import subprocess
import time
import numpy as np  # Imported for structural memory operations and color space math
import cv2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QGraphicsDropShadowEffect,
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider)
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QRectF
from PyQt6.QtGui import QImage, QPixmap, QColor

class CameraThread(QThread):
    # Emits the enhanced GUI-display QImage and the pristine high-res BGR frame for saving
    change_pixmap_signal = pyqtSignal(QImage, object)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # 1. Raspberry Pi Picamera2 stack
        try:
            from picamera2 import Picamera2
            picam = Picamera2()
            # Explicitly request RGB888 format configuration to avoid raw YUV streaming fallbacks
            config = picam.create_preview_configuration(
                main={"size": (4056, 3040), "format": "RGB888"}
            )
            picam.configure(config)
            picam.start()
            
            # Discard initial frames to let the sensor's Auto Exposure and White Balance settle
            self.msleep(600)
            
            while self._run_flag:
                frame = picam.capture_array() 
                if frame is not None:
                    # Fix: Convert incoming BGR frame to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    h, w, ch = frame.shape
                    
                    # Centered crop setup
                    crop_size = min(2500, h, w)
                    start_y = (h - crop_size) // 2
                    start_x = (w - crop_size) // 2
                    
                    # Crop raw frame and force contiguous memory allocation
                    cropped_rgb = np.ascontiguousarray(
                        frame[start_y:start_y+crop_size, start_x:start_x+crop_size]
                    )
                    cropped_bgr = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2BGR)
                    
                    # --- OPTIMIZED PREVIEW PIPELINE ---
                    # Downsample first using INTER_AREA to suppress aliasing and Moiré lines
                    preview_size = 800
                    preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
                    # Dynamic Illumination Boost (CLAHE in LAB color space)
                    lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cl = clahe.apply(l)
                    enhanced_lab = cv2.merge((cl, a, b))
                    preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
                    # Gentle Sharpening (Clinical/Diagnostic grading visual enhancement)
                    sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
                    preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
                    # Final alignment and memory layout stride check
                    preview_rgb = np.ascontiguousarray(preview_rgb)
                    bytes_per_line = preview_rgb.strides[0]
                    
                    q_image = QImage(
                        preview_rgb.data, preview_size, preview_size, bytes_per_line, QImage.Format.Format_RGB888
                    ).copy()
                    
                    self.change_pixmap_signal.emit(q_image, cropped_bgr)
                self.msleep(33)
                
            picam.stop()
            picam.close()

        # 2. Fallback OpenCV VideoCapture
        except ImportError:
            cap = cv2.VideoCapture(0)
            # Enforce MJPG encoding format to prevent falling back to raw interleaved streams
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4056)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3040)
            
            # Sensor Warmup sequence: Read and discard initial frames to stabilize gain and exposure
            for _ in range(15):
                cap.read()
            
            while self._run_flag:
                ret, frame = cap.read()
                if ret:
                    h, w, ch = frame.shape
                    
                    crop_size = min(2500, h, w)
                    start_y = (h - crop_size) // 2
                    start_x = (w - crop_size) // 2
                    
                    # Crop raw frame and force contiguous memory allocation
                    cropped_bgr = np.ascontiguousarray(
                        frame[start_y:start_y+crop_size, start_x:start_x+crop_size]
                    )
                    cropped_rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)
                    
                    # --- OPTIMIZED PREVIEW PIPELINE ---
                    # Downsample first using INTER_AREA to prevent vertical patterns
                    preview_size = 800
                    preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
                    # Dynamic Illumination Boost (CLAHE in LAB space for natural, vivid color)
                    lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cl = clahe.apply(l)
                    enhanced_lab = cv2.merge((cl, a, b))
                    preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
                    # Gentle Sharpening
                    sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
                    preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
                    # Explicit contiguous check and exact memory stride matching
                    preview_rgb = np.ascontiguousarray(preview_rgb)
                    bytes_per_line = preview_rgb.strides[0]
                    
                    q_image = QImage(
                        preview_rgb.data, preview_size, preview_size, bytes_per_line, QImage.Format.Format_RGB888
                    ).copy()
                    
                    self.change_pixmap_signal.emit(q_image, cropped_bgr)
                else:
                    self.change_pixmap_signal.emit(QImage(), None)
                self.msleep(33)
            cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class ZoomableGraphicsView(QGraphicsView):
    # Emits the current zoom level whenever it changes dynamically
    zoom_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        
        # Enable dragging/panning via touchscreen or mouse drag
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.zoom_factor = 1.0
        
        # Stylesheet base design matching dark camera interface
        self.setStyleSheet("""
            QGraphicsView {
                border: 2.5px dashed rgba(109, 40, 217, 0.22); 
                background-color: #000000; 
                border-radius: 16px;
            }
        """)

    def set_image(self, q_image):
        if q_image.isNull():
            self.pixmap_item.setPixmap(QPixmap())
            return
        
        pixmap = QPixmap.fromImage(q_image)
        self.pixmap_item.setPixmap(pixmap)
        # Scale scene limits directly to the incoming image boundaries
        self.scene.setSceneRect(QRectF(pixmap.rect()))

    def set_zoom(self, value):
        self.zoom_factor = max(1.0, min(value, 5.0))
        self.resetTransform()
        self.scale(self.zoom_factor, self.zoom_factor)
        self.zoom_changed.emit(self.zoom_factor)

    def wheelEvent(self, event):
        # Support zooming through physical scroll-wheels
        zoom_step = 1.15 if event.angleDelta().y() > 0 else 0.85
        new_zoom = self.zoom_factor * zoom_step
        self.set_zoom(new_zoom)

    def get_visible_roi(self, original_width, original_height):
        """
        Maps viewport coordinates back to original image coordinates 
        to isolate the cropped zoom sector.
        """
        if self.pixmap_item.pixmap().isNull():
            return None
            
        # Visible boundaries of viewport converted to scene coordinate space
        viewport_rect = self.viewport().rect()
        scene_rect = self.mapToScene(viewport_rect).boundingRect()
        
        img_rect = self.pixmap_item.boundingRect()
        if img_rect.width() <= 0 or img_rect.height() <= 0:
            return None
            
        # Bound coordinates safely inside the preview viewport rectangle
        x_min = max(0.0, scene_rect.left())
        y_min = max(0.0, scene_rect.top())
        x_max = min(img_rect.width(), scene_rect.right())
        y_max = min(img_rect.height(), scene_rect.bottom())
        
        # Translate boundaries based on scale comparison to source array resolution
        scale_x = original_width / img_rect.width()
        scale_y = original_height / img_rect.height()
        
        rx_min = int(x_min * scale_x)
        ry_min = int(y_min * scale_y)
        rx_max = int(x_max * scale_x)
        ry_max = int(y_max * scale_y)
        
        return rx_min, ry_min, rx_max, ry_max


class CameraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Camera Analysis Feed")
        self.setFixedSize(1280, 720) # Expanded height to secure clear spatial gaps
        
        self.last_captured_path = None
        self.current_frame = None
        
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
        self.main_layout.setSpacing(12)
        
        # Top Bar Layout (Glass Back Navigation Button)
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
        
        # High-End Diagnostics Camera Feed Viewport (Zoom-integrated)
        self.camera_view = ZoomableGraphicsView()
        self.camera_view.setFixedSize(550, 550) # Fixed square shape corresponding to raw camera crop layout
        
        # Soft Glow Shadow for the Camera Feed
        shadow_cam = QGraphicsDropShadowEffect(self)
        shadow_cam.setBlurRadius(35)
        shadow_cam.setColor(QColor(109, 40, 217, 25))
        shadow_cam.setOffset(0, 8)
        self.camera_view.setGraphicsEffect(shadow_cam)
        
        self.main_layout.addWidget(self.camera_view, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Zoom Interface Layout
        self.zoom_layout = QHBoxLayout()
        self.zoom_layout.setSpacing(10)
        self.zoom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.zoom_label = QLabel("Zoom: 1.0x")
        self.zoom_label.setStyleSheet("""
            font-family: 'Poppins', sans-serif;
            color: #4C1D95;
            font-size: 13px;
            font-weight: bold;
        """)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setFixedWidth(300)
        self.zoom_slider.setRange(10, 100)  # Maps from 1.0x (10) to 5.0x (50)
        self.zoom_slider.setValue(10)
        self.zoom_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid rgba(109, 40, 217, 0.2);
                height: 8px;
                background: rgba(109, 40, 217, 0.1);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #6D28D9;
                border: 1px solid #5B21B6;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #7C3AED;
            }
        """)
        
        self.zoom_slider.valueChanged.connect(self.on_slider_zoom_changed)
        self.camera_view.zoom_changed.connect(self.on_view_zoom_changed)
        
        self.zoom_layout.addWidget(self.zoom_label)
        self.zoom_layout.addWidget(self.zoom_slider)
        self.main_layout.addLayout(self.zoom_layout)
        
        # Bottom Controls Layout
        self.controls_layout = QHBoxLayout()
        self.controls_layout.setSpacing(15)
        self.controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.controls_layout)
        
        # Base button styling tokens
        btn_style = """
            QPushButton {
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 8px;
                padding: 11px 24px;
                color: white;
                min-width: 160px;
            }
            QPushButton:disabled {
                background-color: rgba(109, 40, 217, 0.08);
                color: rgba(109, 40, 217, 0.35);
                border: 1px solid rgba(109, 40, 217, 0.05);
            }
        """
        
        # Capture Image (Primary Orchid Purple action)
        self.btn_capture = QPushButton("Capture Image")
        self.btn_capture.setStyleSheet(btn_style + """
            QPushButton {
                background-color: #6D28D9;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
        """)
        self.btn_capture.clicked.connect(self.capture_image)
        self.controls_layout.addWidget(self.btn_capture)
        
        # Discard Image (Critical Soft Crimson Action)
        self.btn_discard = QPushButton("Discard Image")
        self.btn_discard.setEnabled(False)
        self.btn_discard.setStyleSheet(btn_style + """
            QPushButton {
                background-color: #EF4444;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:pressed {
                background-color: #B91C1C;
            }
        """)
        self.btn_discard.clicked.connect(self.discard_image)
        self.controls_layout.addWidget(self.btn_discard)
        
        # Proceed (Thematic Gradient Action)
        self.btn_proceed = QPushButton("Proceed")
        self.btn_proceed.setEnabled(False)
        self.btn_proceed.setStyleSheet(btn_style + """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F472B6, 
                    stop:1 #7C3AED);
            }
        """)
        self.btn_proceed.clicked.connect(self.proceed_next)
        self.controls_layout.addWidget(self.btn_proceed)
        
        # Operation Status Notification Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            font-family: 'Poppins', sans-serif;
            color: #10B981; /* Soft Green */
            font-size: 13px; 
            font-weight: bold;
            background: transparent;
        """)
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Thread Initialization
        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_frame)
        self.camera_thread.start()

    def back_to_dashboard(self):
        self.camera_thread.stop()
        subprocess.Popen([sys.executable, "analysis_page1.py"])
        self.close()

    def proceed_next(self):
        self.camera_thread.stop()
        subprocess.Popen([sys.executable, "analysis_page3.py"])
        self.close()

    def on_slider_zoom_changed(self, value):
        factor = value / 10.0
        self.zoom_label.setText(f"Zoom: {factor:.1f}x")
        self.camera_view.set_zoom(factor)

    def on_view_zoom_changed(self, factor):
        # Keeps view trackbars synchronized with manual wheel events
        self.zoom_slider.blockSignals(True)
        self.zoom_slider.setValue(int(factor * 10))
        self.zoom_slider.blockSignals(False)
        self.zoom_label.setText(f"Zoom: {factor:.1f}x")

    def update_frame(self, q_image, cropped_bgr):
        if cropped_bgr is not None and not q_image.isNull():
            self.current_frame = cropped_bgr
            self.camera_view.set_image(q_image)
            self.camera_view.setStyleSheet("""
                QGraphicsView {
                    border: 2.5px dashed rgba(109, 40, 217, 0.22); 
                    background-color: #000000; 
                    border-radius: 16px;
                }
            """)
        else:
            self.camera_view.set_image(QImage())
            self.camera_view.setStyleSheet("""
                QGraphicsView {
                    border: 2px dashed rgba(239, 68, 68, 0.3); 
                    background-color: #000000; 
                    border-radius: 16px;
                }
            """)

    def capture_image(self):
        self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
        self.status_label.clear()
        
        if self.current_frame is None:
            self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
            self.status_label.setText("Error: No live frame to capture.")
            return
            
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"captured_{timestamp}.png"
        filepath = os.path.join(temp_dir, filename)
        
        try:
            # Map coordinates to grab zoomed visible sub-region of raw dimensions
            h, w, ch = self.current_frame.shape
            roi = self.camera_view.get_visible_roi(w, h)
            
            if roi is not None:
                rx_min, ry_min, rx_max, ry_max = roi
                # Extract panned and zoomed-in sub-portion
                frame_to_save = self.current_frame[ry_min:ry_max, rx_min:rx_max]
            else:
                frame_to_save = self.current_frame
                
            if frame_to_save.size == 0:
                frame_to_save = self.current_frame

            # Saves the cropped high quality frame portion
            cv2.imwrite(filepath, frame_to_save)
            self.last_captured_path = filepath
            self.btn_discard.setEnabled(True)
            self.btn_proceed.setEnabled(True)
            self.status_label.setText(f"Success: Image saved to {filepath}")
        except Exception as e:
            self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
            self.status_label.setText(f"Error saving image: {str(e)}")

    def discard_image(self):
        self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
        self.status_label.clear()
        
        if self.last_captured_path and os.path.exists(self.last_captured_path):
            try:
                os.remove(self.last_captured_path)
                self.status_label.setText(f"Discarded: {self.last_captured_path} deleted successfully.")
                self.last_captured_path = None
                self.btn_discard.setEnabled(False)
                self.btn_proceed.setEnabled(False)
            except Exception as e:
                self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
                self.status_label.setText(f"Error discarding file: {str(e)}")
        else:
            self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
            self.status_label.setText("Error: No active image found to discard.")

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    sys.exit(app.exec())