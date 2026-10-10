# # import cv2
# # import numpy as np
# # import time
# # from PIL import Image
# # from PIL import ImageStat
# # from skimage.metrics import structural_similarity as ssim
# # import matplotlib.pyplot as plt


# # cam = cv2.VideoCapture(
# #     0,
# #     cv2.CAP_MSMF
# # )

# # cam.set(
# #     cv2.CAP_PROP_FRAME_WIDTH,
# #     1280
# # )

# # cam.set(
# #     cv2.CAP_PROP_FRAME_HEIGHT,
# #     720
# # )


# # if not cam.isOpened():

# #     print(
# #         "Camera not found"
# #     )

# #     exit()


# # def analyze(path):

# #     pil = Image.open(path)

# #     w,h = pil.size

# #     resolution = w*h

# #     gray_pil = pil.convert(
# #         "L"
# #     )

# #     brightness = ImageStat.Stat(
# #         gray_pil
# #     ).mean[0]

# #     contrast = ImageStat.Stat(
# #         gray_pil
# #     ).stddev[0]

# #     entropy = gray_pil.entropy()

# #     img = cv2.imread(path)

# #     gray = cv2.cvtColor(
# #         img,
# #         cv2.COLOR_BGR2GRAY
# #     )

# #     sharp = cv2.Laplacian(
# #         gray,
# #         cv2.CV_64F
# #     ).var()

# #     blur = cv2.GaussianBlur(
# #         gray,
# #         (5,5),
# #         0
# #     )

# #     noise = np.std(
# #         gray-blur
# #     )

# #     return {

# #         "resolution": resolution,

# #         "brightness": brightness,

# #         "contrast": contrast,

# #         "entropy": entropy,

# #         "sharpness": sharp,

# #         "noise": noise,

# #         "gray": gray

# #     }


# # print(
# #     "Press C = Capture"
# # )

# # print(
# #     "ESC = Exit"
# # )


# # capture = False


# # while True:

# #     ret, frame = cam.read()

# #     if not ret:

# #         continue


# #     gray = cv2.cvtColor(
# #         frame,
# #         cv2.COLOR_BGR2GRAY
# #     )


# #     sharpness = cv2.Laplacian(
# #         gray,
# #         cv2.CV_64F
# #     ).var()


# #     cv2.putText(

# #         frame,

# #         f"Sharp:{sharpness:.2f}",

# #         (20,40),

# #         cv2.FONT_HERSHEY_SIMPLEX,

# #         1,

# #         (0,255,0),

# #         2

# #     )


# #     cv2.imshow(
# #         "Camera Feed",
# #         frame
# #     )


# #     key = cv2.waitKey(1)


# #     if key == ord(
# #         'c'
# #     ):

# #         cv2.imwrite(
# #             "capture1.jpg",
# #             frame
# #         )

# #         print(
# #             "Captured Image 1"
# #         )

# #         time.sleep(2)

# #         ret2, frame2 = cam.read()

# #         cv2.imwrite(
# #             "capture2.jpg",
# #             frame2
# #         )

# #         print(
# #             "Captured Image 2"
# #         )

# #         capture=True

# #         break


# #     if key == 27:

# #         break


# # cam.release()

# # cv2.destroyAllWindows()



# # if capture:

# #     q1 = analyze(
# #         "capture1.jpg"
# #     )

# #     q2 = analyze(
# #         "capture2.jpg"
# #     )


# #     print(
# #         "\n========= RESULT ========="
# #     )


# #     metrics=[

# #         "resolution",

# #         "brightness",

# #         "contrast",

# #         "entropy",

# #         "sharpness",

# #         "noise"

# #     ]


# #     for m in metrics:

# #         print(
# #             "\n",
# #             m
# #         )

# #         print(
# #             "Image1:",
# #             q1[m]
# #         )

# #         print(
# #             "Image2:",
# #             q2[m]
# #         )


# #     similarity = ssim(

# #         q1["gray"],

# #         q2["gray"]

# #     )


# #     print(
# #         "\nSSIM:",
# #         similarity
# #     )


# #     h1 = cv2.calcHist(

# #         [q1["gray"]],

# #         [0],

# #         None,

# #         [256],

# #         [0,256]

# #     )


# #     h2 = cv2.calcHist(

# #         [q2["gray"]],

# #         [0],

# #         None,

# #         [256],

# #         [0,256]

# #     )


# #     plt.figure(
# #         figsize=(10,5)
# #     )

# #     plt.plot(
# #         h1,
# #         label="Capture1"
# #     )

# #     plt.plot(
# #         h2,
# #         label="Capture2"
# #     )

# #     plt.legend()

# #     plt.title(
# #         "Histogram Comparison"
# #     )

# #     plt.show()
    

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
#     QGroupBox, QComboBox, QPushButton, QLabel, QSpinBox, 
#     QMessageBox, QGraphicsDropShadowEffect
# )
# from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
# from PyQt6.QtGui import QImage, QPixmap, QColor


# class CameraThread(QThread):
#     # Emits the enhanced GUI-display QImage and the pristine high-res BGR frame for saving
#     change_pixmap_signal = pyqtSignal(QImage, object)

#     def __init__(self):
#         super().__init__()
#         self._run_flag = True

#     def run(self):
#         # 1. Raspberry Pi Picamera2 stack
#         try:
#             from picamera2 import Picamera2
#             picam = Picamera2()
#             # Request RGB888 format configuration to avoid raw YUV streaming fallbacks
#             config = picam.create_preview_configuration(
#                 main={"size": (4056, 3040), "format": "RGB888"}
#             )
#             picam.configure(config)
#             picam.start()
            
#             # Let the sensor's Auto Exposure and White Balance settle
#             self.msleep(600)
            
#             while self._run_flag:
#                 frame = picam.capture_array() 
#                 if frame is not None:
#                     # Convert BGR frame to RGB color space
#                     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                     h, w, ch = frame.shape
                    
#                     # Centered crop setup
#                     crop_size = min(2500, h, w)
#                     start_y = (h - crop_size) // 2
#                     start_x = (w - crop_size) // 2
                    
#                     # Crop raw frame and force contiguous memory allocation
#                     cropped_rgb = np.ascontiguousarray(
#                         frame[start_y:start_y+crop_size, start_x:start_x+crop_size]
#                     )
#                     cropped_bgr = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2BGR)
                    
#                     # --- PREVIEW PIPELINE ---
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
            
#             # Sensor Warmup sequence
#             for _ in range(15):
#                 cap.read()
            
#             while self._run_flag:
#                 ret, frame = cap.read()
#                 if ret:
#                     h, w, ch = frame.shape
                    
#                     crop_size = min(2500, h, w)
#                     start_y = (h - crop_size) // 2
#                     start_x = (w - crop_size) // 2
                    
#                     # Crop raw frame and force contiguous memory allocation
#                     cropped_bgr = np.ascontiguousarray(
#                         frame[start_y:start_y+crop_size, start_x:start_x+crop_size]
#                     )
#                     cropped_rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)
                    
#                     # --- PREVIEW PIPELINE ---
#                     preview_size = 800
#                     preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
#                     # Dynamic Illumination Boost (CLAHE in LAB space)
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
        
#         # Central Widget & Soft Lavender/Orchid Gradient Background
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
        
#         # Main Layout Setup
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(25, 15, 25, 15)
#         self.main_layout.setSpacing(10)
        
#         # Top Bar (Back Button)
#         self.top_bar = QHBoxLayout()
#         self.btn_back = QPushButton("← Back")
#         self.btn_back.setFixedSize(110, 38)
#         self.btn_back.setStyleSheet("""
#             QPushButton {
#                 background-color: rgba(109, 40, 217, 0.08);
#                 border: 1px solid rgba(109, 40, 217, 0.18);
#                 color: #4C1D95;
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
        
#         # Workspace Splitting: Left Controls & Right Stream Viewport
#         self.content_layout = QHBoxLayout()
#         self.content_layout.setSpacing(20)
#         self.main_layout.addLayout(self.content_layout)
        
#         self.left_panel = QVBoxLayout()
#         self.left_panel.setSpacing(12)
#         self.content_layout.addLayout(self.left_panel, stretch=1)
        
#         self.right_panel = QVBoxLayout()
#         self.right_panel.setSpacing(12)
#         self.content_layout.addLayout(self.right_panel, stretch=3)
        
#         # Setup Widgets
#         self.setup_left_panel()
#         self.setup_right_panel()
        
#         # Timers and Threads
#         self.serial_timer = QTimer()
#         self.serial_timer.timeout.connect(self.read_serial_data)

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
#                 border-radius: 12px;
#                 margin-top: 10px;
#                 background-color: rgba(255, 255, 255, 0.72);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 12px;
#                 padding: 0 5px;
#             }
#             QLabel {
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 12px;
#                 color: #4C1D95;
#                 font-weight: 500;
#             }
#         """
        
#         input_style = """
#             QComboBox, QSpinBox {
#                 border: 1px solid rgba(109, 40, 217, 0.18);
#                 border-radius: 6px;
#                 padding: 5px 10px;
#                 background-color: rgba(255, 255, 255, 0.9);
#                 color: #2E1065;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 12px;
#             }
#             QComboBox:focus, QSpinBox:focus {
#                 border: 1.5px solid #6D28D9;
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
#                 border-radius: 6px;
#                 padding: 7px;
#                 font-size: 12px;
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

#         # Serial Connection Setup
#         self.conn_group = QGroupBox("Serial Connection")
#         self.conn_group.setStyleSheet(group_style)
#         conn_layout = QHBoxLayout(self.conn_group)
#         conn_layout.setContentsMargins(12, 20, 12, 12)
        
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

#         # X-Axis Servo Controller Group
#         self.s1_group = QGroupBox("Left Right Control (X-Axis)")
#         self.s1_group.setStyleSheet(group_style)
#         s1_layout = QVBoxLayout(self.s1_group)
#         s1_layout.setContentsMargins(12, 20, 12, 12)
#         s1_layout.setSpacing(8)
        
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

#         # Y-Axis Servo Controller Group
#         self.s2_group = QGroupBox("Up Down Control (Y-Axis)")
#         self.s2_group.setStyleSheet(group_style)
#         s2_layout = QVBoxLayout(self.s2_group)
#         s2_layout.setContentsMargins(12, 20, 12, 12)
#         s2_layout.setSpacing(8)
        
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
#                 margin-top: 10px;
#                 background-color: rgba(255, 255, 255, 0.72);
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 12px;
#                 padding: 0 5px;
#             }
#         """
        
#         # Stream Viewport Area
#         self.cam_group = QGroupBox("Enlarged Diagnostic Viewport")
#         self.cam_group.setStyleSheet(group_style)
#         cam_layout = QVBoxLayout(self.cam_group)
#         cam_layout.setContentsMargins(15, 20, 15, 15)
        
#         self.camera_label = QLabel("Loading Camera Stream...")
#         self.camera_label.setFixedSize(1000, 600)
#         self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.camera_label.setStyleSheet("""
#             QLabel {
#                 border: 2.5px dashed rgba(109, 40, 217, 0.22); 
#                 background-color: #000000; 
#                 border-radius: 16px;
#                 color: #C084FC;
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 14px;
#             }
#         """)
        
#         # Stream Drop Shadow
#         shadow_cam = QGraphicsDropShadowEffect(self)
#         shadow_cam.setBlurRadius(35)
#         shadow_cam.setColor(QColor(109, 40, 217, 25))
#         shadow_cam.setOffset(0, 8)
#         self.camera_label.setGraphicsEffect(shadow_cam)
#         cam_layout.addWidget(self.camera_label, alignment=Qt.AlignmentFlag.AlignCenter)
#         self.right_panel.addWidget(self.cam_group)

#         # Diagnostics Capture, Discard and Progression Control Box
#         self.controls_layout = QHBoxLayout()
#         self.controls_layout.setSpacing(15)
#         self.controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.right_panel.addLayout(self.controls_layout)
        
#         btn_action_style = """
#             QPushButton {
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-weight: bold;
#                 font-size: 14px;
#                 border: none;
#                 border-radius: 8px;
#                 padding: 11px 24px;
#                 color: white;
#                 min-width: 160px;
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
#         self.controls_layout.addWidget(self.btn_capture)
        
#         self.btn_discard = QPushButton("Discard Image")
#         self.btn_discard.setEnabled(False)
#         self.btn_discard.setStyleSheet(btn_action_style + """
#             QPushButton { background-color: #EF4444; }
#             QPushButton:hover { background-color: #DC2626; }
#             QPushButton:pressed { background-color: #B91C1C; }
#         """)
#         self.btn_discard.clicked.connect(self.discard_image)
#         self.controls_layout.addWidget(self.btn_discard)
        
#         self.btn_proceed = QPushButton("Proceed")
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
#         self.controls_layout.addWidget(self.btn_proceed)
        
#         # Operational Notification Banner
#         self.status_label = QLabel("")
#         self.status_label.setStyleSheet("""
#             font-family: 'Poppins', sans-serif;
#             color: #10B981;
#             font-size: 13px; 
#             font-weight: bold;
#             background: transparent;
#         """)
#         self.right_panel.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

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
#                 1000, 600, 
#                 Qt.AspectRatioMode.KeepAspectRatio, 
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self.camera_label.setPixmap(pixmap)
#             self.camera_label.setStyleSheet("""
#                 QLabel {
#                     border: 2.5px dashed rgba(109, 40, 217, 0.22); 
#                     background-color: #000000; 
#                     border-radius: 16px;
#                 }
#             """)
#         else:
#             self.camera_label.setPixmap(QPixmap())
#             self.camera_label.setText("No camera device found/accessible.")
#             self.camera_label.setStyleSheet("""
#                 color: #EF4444; 
#                 font-family: 'Poppins', sans-serif;
#                 font-size: 18px; 
#                 font-weight: bold; 
#                 border: 2px dashed rgba(239, 68, 68, 0.3); 
#                 background-color: #000000; 
#                 border-radius: 16px;
#             """)

#     def capture_image(self):
#         self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#         self.status_label.clear()
        
#         if self.current_frame is None:
#             self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#             self.status_label.setText("Error: No live frame to capture.")
#             return
            
#         temp_dir = "temp"
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
            
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         filename = f"captured_{timestamp}.png"
#         filepath = os.path.join(temp_dir, filename)
        
#         try:
#             cv2.imwrite(filepath, self.current_frame)
#             self.last_captured_path = filepath
#             self.btn_discard.setEnabled(True)
#             self.btn_proceed.setEnabled(True)
#             self.status_label.setText(f"Success: Image saved to {filepath}")
#         except Exception as e:
#             self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#             self.status_label.setText(f"Error saving image: {str(e)}")

#     def discard_image(self):
#         self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#         self.status_label.clear()
        
#         if self.last_captured_path and os.path.exists(self.last_captured_path):
#             try:
#                 os.remove(self.last_captured_path)
#                 self.status_label.setText(f"Discarded: {self.last_captured_path} deleted successfully.")
#                 self.last_captured_path = None
#                 self.btn_discard.setEnabled(False)
#                 self.btn_proceed.setEnabled(False)
#             except Exception as e:
#                 self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#                 self.status_label.setText(f"Error discarding file: {str(e)}")
#         else:
#             self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
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
#                 time.sleep(2)  # Wait for Arduino setup cycle
#                 self.ser.reset_input_buffer()
                
#                 self.connect_btn.setText("Disconnect")
#                 self.connect_btn.setStyleSheet("""
#                     QPushButton {
#                         background-color: #EF4444; 
#                         color: white; 
#                         font-family: 'Poppins', sans-serif;
#                         font-weight: bold; 
#                         border: none;
#                         border-radius: 6px; 
#                         padding: 7px;
#                     }
#                     QPushButton:hover {
#                         background-color: #DC2626;
#                     }
#                 """)
#                 self.set_controls_enabled(True)
#                 self.serial_timer.start(50)
#                 self.status_label.setText(f"Serial Connection Established: {port}")
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
#                     border-radius: 6px; 
#                     padding: 7px;
#                 }
#                 QPushButton:hover {
#                     background-color: #059669;
#                 }
#             """)
#             self.set_controls_enabled(False)
#             self.status_label.setText("Serial Connection Closed.")

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
#                 self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#                 self.status_label.setText(f"Serial Write Fail: {e}")
#                 self.toggle_connection()

#     def read_serial_data(self):
#         if self.ser and self.ser.is_open:
#             try:
#                 while self.ser.in_waiting > 0:
#                     line = self.ser.readline().decode('utf-8').strip()
#                     if line:
#                         # Log signals can optionally write to the status bar if required
#                         self.status_label.setText(f"Hardware response: {line}")
#             except Exception as e:
#                 self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
#                 self.status_label.setText(f"Serial Read Fail: {e}")
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
import time
import os
import subprocess
import numpy as np  # Imported for fast array manipulation and scaling operations
import serial
import serial.tools.list_ports
import cv2

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGroupBox, QComboBox, QPushButton, QLabel, QSpinBox, QTextEdit, 
    QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QColor

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # 1. Picamera2 Path (Raspberry Pi Native)
        try:
            from picamera2 import Picamera2
            picam = Picamera2()
            
            # Explicitly configure "RGB888" to prevent YUV/Raw format fallback issues
            config = picam.create_preview_configuration(
                main={"size": (4056, 3040), "format": "RGB888"}
            )
            picam.configure(config)
            picam.start()
            
            # Allow sensor auto-exposure and white balance to stabilize
            self.msleep(500)
            
            while self._run_flag:
                frame = picam.capture_array() 
                if frame is not None:
                    # Convert BGR to RGB to fix the bluish tone
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    h, w, ch = rgb_frame.shape
                    
                    # Calculate center coordinates for a square crop
                    crop_size = min(2200, h, w)
                    start_y = (h - crop_size) // 2
                    start_x = (w - crop_size) // 2
                    cropped = rgb_frame[start_y:start_y+crop_size, start_x:start_x+crop_size].copy()
                    
                    # Digital gain adjustment: Fixes dimness by scaling brightness/contrast
                    # alpha = contrast boost (1.0 - 1.3), beta = brightness boost (0 - 100)
                    enhanced = cv2.convertScaleAbs(cropped, alpha=1.15, beta=15)
                    
                    # Downsample using cv2.INTER_AREA to eliminate aliasing/pattern noise
                    resized = cv2.resize(enhanced, (420, 420), interpolation=cv2.INTER_AREA)
                    
                    ch_h, ch_w, ch_ch = resized.shape
                    bytes_per_line = ch_ch * ch_w
                    
                    # Create a contiguous QImage copy
                    convert_to_Qt_format = QImage(
                        resized.data, ch_w, ch_h, bytes_per_line, QImage.Format.Format_RGB888
                    ).copy()
                    
                    self.change_pixmap_signal.emit(convert_to_Qt_format)
                self.msleep(33)
                
            picam.stop()
            picam.close()

        # 2. OpenCV Fallback Path (Webcam / Standard Driver)
        except ImportError:
            cap = cv2.VideoCapture(0)
            
            # Force MJPG codec to ensure the camera driver decodes standard BGR color ranges
            # and prevents bandwith-limited fallback to noisy/raw YUV streams
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4056)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3040)
            
            # Allow camera sensor Warmup
            self.msleep(500)
            
            while self._run_flag:
                ret, cv_img = cap.read()
                if ret:
                    # Convert default BGR to RGB color space
                    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    
                    # Calculate center coordinates for a square crop
                    crop_size = min(2200, h, w)
                    start_y = (h - crop_size) // 2
                    start_x = (w - crop_size) // 2
                    cropped = rgb_image[start_y:start_y+crop_size, start_x:start_x+crop_size].copy()
                    
                    # Digital gain adjustment: Fixes dimness
                    enhanced = cv2.convertScaleAbs(cropped, alpha=1.15, beta=15)
                    
                    # Downsample using cv2.INTER_AREA to mathematically eliminate pattern lines
                    resized = cv2.resize(enhanced, (520, 520), interpolation=cv2.INTER_AREA)
                    
                    ch_h, ch_w, ch_ch = resized.shape
                    bytes_per_line = ch_ch * ch_w
                    
                    convert_to_Qt_format = QImage(
                        resized.data, ch_w, ch_h, bytes_per_line, QImage.Format.Format_RGB888
                    ).copy()
                    
                    self.change_pixmap_signal.emit(convert_to_Qt_format)
                self.msleep(33)
            cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class ArduinoControllerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.setWindowTitle("OncoVue - Hardware Controller")
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
        self.main_layout.setContentsMargins(25, 20, 25, 20)
        self.main_layout.setSpacing(10)
        
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
        
        # Split workspace layouts
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(15)
        self.main_layout.addLayout(self.content_layout)
        
        self.left_panel = QVBoxLayout()
        self.left_panel.setSpacing(8)
        self.content_layout.addLayout(self.left_panel, stretch=1)
        
        self.right_panel = QVBoxLayout()
        self.right_panel.setSpacing(8)
        self.content_layout.addLayout(self.right_panel, stretch=2)
        
        self.setup_left_panel()
        self.setup_right_panel()
        
        self.serial_timer = QTimer()
        self.serial_timer.timeout.connect(self.read_serial_data)

        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.start()

    def back_to_dashboard(self):
        self.camera_thread.stop()
        if self.ser and self.ser.is_open:
            self.ser.close()
        subprocess.Popen([sys.executable, "page3.py"])
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
                margin-top: 5px;
                background-color: rgba(255, 255, 255, 0.72);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }
            QLabel {
                font-family: 'Poppins', sans-serif;
                font-size: 12px;
                color: #4C1D95; /* Velvet Slate label */
                font-weight: 500;
            }
        """
        
        input_style = """
            QComboBox, QSpinBox {
                border: 1px solid rgba(109, 40, 217, 0.18);
                border-radius: 6px;
                padding: 4px 10px;
                background-color: rgba(255, 255, 255, 0.9);
                color: #2E1065; /* Deep Amethyst */
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 12px;
            }
            QComboBox:focus, QSpinBox:focus {
                border: 1.5px solid #6D28D9;
                background-color: #ffffff;
            }
        """
        
        btn_style = """
            QPushButton {
                background-color: rgba(192, 132, 252, 0.12);
                border: 1px solid rgba(192, 132, 252, 0.25);
                color: #4C1D95;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(192, 132, 252, 0.22);
                border-color: rgba(192, 132, 252, 0.4);
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(109, 40, 217, 0.08);
                color: #C084FC;
            }
        """
        
        self.conn_group = QGroupBox("Serial Connection")
        self.conn_group.setStyleSheet(group_style)
        conn_layout = QHBoxLayout(self.conn_group)
        conn_layout.setContentsMargins(12, 15, 12, 10)
        
        self.port_combo = QComboBox()
        self.port_combo.setStyleSheet(input_style)
        self.refresh_ports()
        conn_layout.addWidget(self.port_combo)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet(btn_style)
        self.refresh_btn.clicked.connect(self.refresh_ports)
        conn_layout.addWidget(self.refresh_btn)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet(btn_style + "QPushButton{background-color: #10B981; color: white; border: none;} QPushButton:hover{background-color: #059669;}")
        self.connect_btn.clicked.connect(self.toggle_connection)
        conn_layout.addWidget(self.connect_btn)
        self.left_panel.addWidget(self.conn_group)

        self.s1_group = QGroupBox("Left Right Control(X axis)")
        self.s1_group.setStyleSheet(group_style)
        s1_layout = QVBoxLayout(self.s1_group)
        s1_layout.setContentsMargins(12, 15, 12, 10)
        s1_layout.setSpacing(6)
        
        step_lay1 = QHBoxLayout()
        step_lay1.addWidget(QLabel("Step Size:"))
        self.s1_step = QSpinBox()
        self.s1_step.setStyleSheet(input_style)
        self.s1_step.setRange(1, 1800)
        self.s1_step.setValue(90)
        step_lay1.addWidget(self.s1_step)
        s1_layout.addLayout(step_lay1)
        
        btn_lay1 = QHBoxLayout()
        self.s1_left_btn = QPushButton("- Custom")
        self.s1_left_btn.setStyleSheet(btn_style)
        self.s1_left_btn.clicked.connect(lambda: self.send_servo_command("s1", "left", self.s1_step.value()))
        self.s1_right_btn = QPushButton("+ Custom")
        self.s1_right_btn.setStyleSheet(btn_style)
        self.s1_right_btn.clicked.connect(lambda: self.send_servo_command("s1", "right", self.s1_step.value()))
        btn_lay1.addWidget(self.s1_left_btn)
        btn_lay1.addWidget(self.s1_right_btn)
        s1_layout.addLayout(btn_lay1)

        fast_lay1 = QHBoxLayout()
        self.s1_m20 = QPushButton("- 20°")
        self.s1_m20.setStyleSheet(btn_style)
        self.s1_m20.clicked.connect(lambda: self.send_servo_command("s1", "left", 20))
        self.s1_p20 = QPushButton("+ 20°")
        self.s1_p20.setStyleSheet(btn_style)
        self.s1_p20.clicked.connect(lambda: self.send_servo_command("s1", "right", 20))
        fast_lay1.addWidget(self.s1_m20)
        fast_lay1.addWidget(self.s1_p20)
        s1_layout.addLayout(fast_lay1)
        self.left_panel.addWidget(self.s1_group)

        self.s2_group = QGroupBox("Up Down Control(Y axis)")
        self.s2_group.setStyleSheet(group_style)
        s2_layout = QVBoxLayout(self.s2_group)
        s2_layout.setContentsMargins(12, 15, 12, 10)
        s2_layout.setSpacing(6)
        
        step_lay2 = QHBoxLayout()
        step_lay2.addWidget(QLabel("Step Size:"))
        self.s2_step = QSpinBox()
        self.s2_step.setStyleSheet(input_style)
        self.s2_step.setRange(1, 1800)
        self.s2_step.setValue(90)
        step_lay2.addWidget(self.s2_step)
        s2_layout.addLayout(step_lay2)
        
        btn_lay2 = QHBoxLayout()
        self.s2_left_btn = QPushButton("- Custom")
        self.s2_left_btn.setStyleSheet(btn_style)
        self.s2_left_btn.clicked.connect(lambda: self.send_servo_command("s2", "left", self.s2_step.value()))
        self.s2_right_btn = QPushButton("+ Custom")
        self.s2_right_btn.setStyleSheet(btn_style)
        self.s2_right_btn.clicked.connect(lambda: self.send_servo_command("s2", "right", self.s2_step.value()))
        btn_lay2.addWidget(self.s2_left_btn)
        btn_lay2.addWidget(self.s2_right_btn)
        s2_layout.addLayout(btn_lay2)

        fast_lay2 = QHBoxLayout()
        self.s2_m20 = QPushButton("- 20°")
        self.s2_m20.setStyleSheet(btn_style)
        self.s2_m20.clicked.connect(lambda: self.send_servo_command("s2", "left", 20))
        self.s2_p20 = QPushButton("+ 20°")
        self.s2_p20.setStyleSheet(btn_style)
        self.s2_p20.clicked.connect(lambda: self.send_servo_command("s2", "right", 20))
        fast_lay2.addWidget(self.s2_m20)
        fast_lay2.addWidget(self.s2_p20)
        s2_layout.addLayout(fast_lay2)
        self.left_panel.addWidget(self.s2_group)

        self.nav_group = QGroupBox("Navigation")
        self.nav_group.setStyleSheet(group_style)
        nav_layout = QVBoxLayout(self.nav_group)
        nav_layout.setContentsMargins(12, 15, 12, 10)
        
        self.page2_btn = QPushButton("Proceed to Analysis")
        self.page2_btn.setMinimumHeight(45)
        self.page2_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #EC4899, 
                    stop:1 #6D28D9); /* Rose to Orchid gradient */
                color: white; 
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold; 
                font-size: 13px; 
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #F472B6, 
                    stop:1 #7C3AED);
            }
        """)
        self.page2_btn.clicked.connect(self.launch_page2)
        nav_layout.addWidget(self.page2_btn)
        self.left_panel.addWidget(self.nav_group)
        
        self.set_controls_enabled(False)

    def setup_right_panel(self):
        group_style = """
            QGroupBox {
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 11px;
                color: #6D28D9;
                font-weight: bold;
                border: 1px solid rgba(109, 40, 217, 0.15);
                border-radius: 12px;
                margin-top: 5px;
                background-color: rgba(255, 255, 255, 0.72);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }
        """
        
        # Camera Stream: Viewport increased in dimensions from space savings
        self.cam_group = QGroupBox("Camera Stream")
        self.cam_group.setStyleSheet(group_style)
        cam_layout = QVBoxLayout(self.cam_group)
        cam_layout.setContentsMargins(12, 15, 12, 12)
        
        self.image_label = QLabel("Loading HQ Camera...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #000000; 
            border: 2px dashed rgba(109, 40, 217, 0.18); 
            border-radius: 8px; 
            color: #C084FC;
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
        """)
        # Expanded square profile to match thread output natively
        self.image_label.setFixedSize(520, 520)
        cam_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.right_panel.addWidget(self.cam_group)

        # Hardware Log: Adjusted layout to exactly 2 lines
        self.log_group = QGroupBox("Hardware Log")
        self.log_group.setStyleSheet(group_style)
        log_layout = QVBoxLayout(self.log_group)
        log_layout.setContentsMargins(12, 15, 12, 10)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        # Reduced vertical size to make the log exactly 2 lines high
        self.log_text.setFixedHeight(55)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(46, 16, 101, 0.05); /* Soft deep amethyst opacity tint */
                color: #6D28D9; /* Orchid terminal font */
                border: 1px solid rgba(109, 40, 217, 0.15); 
                font-family: 'Courier New', monospace; 
                font-size: 12px;
                border-radius: 8px;
                padding: 5px 10px;
            }
        """)
        log_layout.addWidget(self.log_text)
        self.right_panel.addWidget(self.log_group)

        shadow_cam = QGraphicsDropShadowEffect(self)
        shadow_cam.setBlurRadius(25)
        shadow_cam.setColor(QColor(109, 40, 217, 15))
        self.cam_group.setGraphicsEffect(shadow_cam)

        shadow_log = QGraphicsDropShadowEffect(self)
        shadow_log.setBlurRadius(25)
        shadow_log.setColor(QColor(109, 40, 217, 15))
        self.log_group.setGraphicsEffect(shadow_log)

    def update_image(self, q_img):
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def refresh_ports(self):
        self.port_combo.clear()
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            self.port_combo.addItem(port.device)

    def toggle_connection(self):
        if self.ser is None:
            port = self.port_combo.currentText()
            if not port:
                QMessageBox.warning(self, "Warning", "Select serial port first.")
                return
            try:
                self.ser = serial.Serial(port, 9600, timeout=0.1)
                time.sleep(2)
                self.ser.reset_input_buffer()
                
                self.log_text.append(f"Connected on: {port}")
                self.connect_btn.setText("Disconnect")
                self.connect_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #EF4444; /* Soft Crimson */
                        color: white; 
                        font-family: 'Poppins', sans-serif;
                        font-weight: bold; 
                        border: none;
                        border-radius: 6px; 
                        padding: 7px;
                    }
                    QPushButton:hover {
                        background-color: #DC2626;
                    }
                """)
                self.set_controls_enabled(True)
                self.serial_timer.start(50)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open port: {e}")
                self.ser = None
        else:
            self.serial_timer.stop()
            try:
                self.ser.close()
            except:
                pass
            self.ser = None
            self.log_text.append("Serial disconnected.")
            self.connect_btn.setText("Connect")
            self.connect_btn.setStyleSheet("""
                QPushButton {
                    background-color: #10B981; /* Soft Mint Green */
                    color: white; 
                    font-family: 'Poppins', sans-serif;
                    font-weight: bold; 
                    border: none;
                    border-radius: 6px; 
                    padding: 7px;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """)
            self.set_controls_enabled(False)

    def set_controls_enabled(self, enabled):
        self.s1_left_btn.setEnabled(enabled)
        self.s1_right_btn.setEnabled(enabled)
        self.s1_m20.setEnabled(enabled)
        self.s1_p20.setEnabled(enabled)
        self.s2_left_btn.setEnabled(enabled)
        self.s2_right_btn.setEnabled(enabled)
        self.s2_m20.setEnabled(enabled)
        self.s2_p20.setEnabled(enabled)

    def send_servo_command(self, servo_id, direction, degrees):
        self.write_to_serial(f"{servo_id} {direction} {degrees}\n")

    def launch_page2(self):
        if self.ser and self.ser.is_open:
            self.toggle_connection()
            self.log_text.append("Released serial port connection.")

        self.log_text.append("Launching analysis page2.py...")
        self.camera_thread.stop()
        
        try:
            subprocess.Popen([sys.executable, "analysis_page2.py"])
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not launch page2.py: {e}")

    def write_to_serial(self, command):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(command.encode('utf-8'))
            except Exception as e:
                self.log_text.append(f"[Write Fail]: {e}")
                self.toggle_connection()

    def read_serial_data(self):
        if self.ser and self.ser.is_open:
            try:
                while self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        self.log_text.append(f"[Arduino]: {line}")
            except Exception as e:
                self.log_text.append(f"[Read Fail]: {e}")
                self.toggle_connection()

    def closeEvent(self, event):
        self.camera_thread.stop()
        if self.ser and self.ser.is_open:
            self.ser.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ArduinoControllerGUI()
    gui.show()
    sys.exit(app.exec())