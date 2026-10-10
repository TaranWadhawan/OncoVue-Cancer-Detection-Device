
# import sys
# import os
# import subprocess
# import time
# import numpy as np  # Imported for structural memory operations and color space math
# import cv2
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
#                              QHBoxLayout, QWidget, QPushButton, QGraphicsDropShadowEffect,
#                              QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider)
# from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QRectF
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
#             # Explicitly request RGB888 format configuration to avoid raw YUV streaming fallbacks
#             config = picam.create_preview_configuration(
#                 main={"size": (4056, 3040), "format": "RGB888"}
#             )
#             picam.configure(config)
#             picam.start()
            
#             # Discard initial frames to let the sensor's Auto Exposure and White Balance settle
#             self.msleep(600)
            
#             while self._run_flag:
#                 frame = picam.capture_array() 
#                 if frame is not None:
#                     # Fix: Convert incoming BGR frame to RGB
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
                    
#                     # --- OPTIMIZED PREVIEW PIPELINE ---
#                     # Downsample first using INTER_AREA to suppress aliasing and Moiré lines
#                     preview_size = 800
#                     preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
#                     # Dynamic Illumination Boost (CLAHE in LAB color space)
#                     lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
#                     l, a, b = cv2.split(lab)
#                     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#                     cl = clahe.apply(l)
#                     enhanced_lab = cv2.merge((cl, a, b))
#                     preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
#                     # Gentle Sharpening (Clinical/Diagnostic grading visual enhancement)
#                     sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
#                     preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
#                     # Final alignment and memory layout stride check
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
#             # Enforce MJPG encoding format to prevent falling back to raw interleaved streams
#             cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
#             cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4056)
#             cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3040)
            
#             # Sensor Warmup sequence: Read and discard initial frames to stabilize gain and exposure
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
                    
#                     # --- OPTIMIZED PREVIEW PIPELINE ---
#                     # Downsample first using INTER_AREA to prevent vertical patterns
#                     preview_size = 800
#                     preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
#                     # Dynamic Illumination Boost (CLAHE in LAB space for natural, vivid color)
#                     lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
#                     l, a, b = cv2.split(lab)
#                     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#                     cl = clahe.apply(l)
#                     enhanced_lab = cv2.merge((cl, a, b))
#                     preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
#                     # Gentle Sharpening
#                     sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
#                     preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
#                     # Explicit contiguous check and exact memory stride matching
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


# class ZoomableGraphicsView(QGraphicsView):
#     # Emits the current zoom level whenever it changes dynamically
#     zoom_changed = pyqtSignal(float)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.scene = QGraphicsScene(self)
#         self.setScene(self.scene)
        
#         self.pixmap_item = QGraphicsPixmapItem()
#         self.scene.addItem(self.pixmap_item)
        
#         # Enable dragging/panning via touchscreen or mouse drag
#         self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
#         self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
#         self.zoom_factor = 1.0
        
#         # Stylesheet base design matching dark camera interface
#         self.setStyleSheet("""
#             QGraphicsView {
#                 border: 2.5px dashed rgba(109, 40, 217, 0.22); 
#                 background-color: #000000; 
#                 border-radius: 16px;
#             }
#         """)

#     def set_image(self, q_image):
#         if q_image.isNull():
#             self.pixmap_item.setPixmap(QPixmap())
#             return
        
#         pixmap = QPixmap.fromImage(q_image)
#         self.pixmap_item.setPixmap(pixmap)
#         # Scale scene limits directly to the incoming image boundaries
#         self.scene.setSceneRect(QRectF(pixmap.rect()))

#     def set_zoom(self, value):
#         self.zoom_factor = max(1.0, min(value, 10.0))
#         self.resetTransform()
#         self.scale(self.zoom_factor, self.zoom_factor)
#         self.zoom_changed.emit(self.zoom_factor)

#     def wheelEvent(self, event):
#         # Support zooming through physical scroll-wheels
#         zoom_step = 1.15 if event.angleDelta().y() > 0 else 0.85
#         new_zoom = self.zoom_factor * zoom_step
#         self.set_zoom(new_zoom)

#     def get_visible_roi(self, original_width, original_height):
#         """
#         Maps viewport coordinates back to original image coordinates 
#         to isolate the cropped zoom sector.
#         """
#         if self.pixmap_item.pixmap().isNull():
#             return None
            
#         # Visible boundaries of viewport converted to scene coordinate space
#         viewport_rect = self.viewport().rect()
#         scene_rect = self.mapToScene(viewport_rect).boundingRect()
        
#         img_rect = self.pixmap_item.boundingRect()
#         if img_rect.width() <= 0 or img_rect.height() <= 0:
#             return None
            
#         # Bound coordinates safely inside the preview viewport rectangle
#         x_min = max(0.0, scene_rect.left())
#         y_min = max(0.0, scene_rect.top())
#         x_max = min(img_rect.width(), scene_rect.right())
#         y_max = min(img_rect.height(), scene_rect.bottom())
        
#         # Translate boundaries based on scale comparison to source array resolution
#         scale_x = original_width / img_rect.width()
#         scale_y = original_height / img_rect.height()
        
#         rx_min = int(x_min * scale_x)
#         ry_min = int(y_min * scale_y)
#         rx_max = int(x_max * scale_x)
#         ry_max = int(y_max * scale_y)
        
#         return rx_min, ry_min, rx_max, ry_max


# class CameraWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("OncoVue - Camera Analysis Feed")
#         self.setFixedSize(1280, 720) # Expanded height to secure clear spatial gaps
        
#         self.last_captured_path = None
#         self.current_frame = None
        
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
#         self.main_layout.setSpacing(12)
        
#         # Top Bar Layout (Glass Back Navigation Button)
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
        
#         # High-End Diagnostics Camera Feed Viewport (Zoom-integrated)
#         self.camera_view = ZoomableGraphicsView()
#         self.camera_view.setFixedSize(550, 550) # Fixed square shape corresponding to raw camera crop layout
        
#         # Soft Glow Shadow for the Camera Feed
#         shadow_cam = QGraphicsDropShadowEffect(self)
#         shadow_cam.setBlurRadius(35)
#         shadow_cam.setColor(QColor(109, 40, 217, 25))
#         shadow_cam.setOffset(0, 8)
#         self.camera_view.setGraphicsEffect(shadow_cam)
        
#         self.main_layout.addWidget(self.camera_view, alignment=Qt.AlignmentFlag.AlignCenter)
        
#         # Zoom Interface Layout
#         self.zoom_layout = QHBoxLayout()
#         self.zoom_layout.setSpacing(10)
#         self.zoom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
#         self.zoom_label = QLabel("Zoom: 1.0x")
#         self.zoom_label.setStyleSheet("""
#             font-family: 'Poppins', sans-serif;
#             color: #4C1D95;
#             font-size: 13px;
#             font-weight: bold;
#         """)
        
#         self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
#         self.zoom_slider.setFixedWidth(300)
#         self.zoom_slider.setMinimum(10)  # Representing 1.0x
#         self.zoom_slider.setMaximum(100)  # Representing 4.0x
#         self.zoom_slider.setRange(10, 100)  # Maps from 1.0x (10) to 5.0x (50)
#         self.zoom_slider.setValue(10)
#         self.zoom_slider.setStyleSheet("""
#             QSlider::groove:horizontal {
#                 border: 1px solid rgba(109, 40, 217, 0.2);
#                 height: 8px;
#                 background: rgba(109, 40, 217, 0.1);
#                 border-radius: 4px;
#             }
#             QSlider::handle:horizontal {
#                 background: #6D28D9;
#                 border: 1px solid #5B21B6;
#                 width: 18px;
#                 height: 18px;
#                 margin: -5px 0;
#                 border-radius: 9px;
#             }
#             QSlider::handle:horizontal:hover {
#                 background: #7C3AED;
#             }
#         """)
        
#         self.zoom_slider.valueChanged.connect(self.on_slider_zoom_changed)
#         self.camera_view.zoom_changed.connect(self.on_view_zoom_changed)
        
#         self.zoom_layout.addWidget(self.zoom_label)
#         self.zoom_layout.addWidget(self.zoom_slider)
#         self.main_layout.addLayout(self.zoom_layout)
        
#         # Bottom Controls Layout
#         self.controls_layout = QHBoxLayout()
#         self.controls_layout.setSpacing(15)
#         self.controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.main_layout.addLayout(self.controls_layout)
        
#         # Base button styling tokens
#         btn_style = """
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
        
#         # Capture Image (Primary Orchid Purple action)
#         self.btn_capture = QPushButton("Capture Image")
#         self.btn_capture.setStyleSheet(btn_style + """
#             QPushButton {
#                 background-color: #6D28D9;
#             }
#             QPushButton:hover {
#                 background-color: #7C3AED;
#             }
#             QPushButton:pressed {
#                 background-color: #5B21B6;
#             }
#         """)
#         self.btn_capture.clicked.connect(self.capture_image)
#         self.controls_layout.addWidget(self.btn_capture)
        
#         # Discard Image (Critical Soft Crimson Action)
#         self.btn_discard = QPushButton("Discard Image")
#         self.btn_discard.setEnabled(False)
#         self.btn_discard.setStyleSheet(btn_style + """
#             QPushButton {
#                 background-color: #EF4444;
#             }
#             QPushButton:hover {
#                 background-color: #DC2626;
#             }
#             QPushButton:pressed {
#                 background-color: #B91C1C;
#             }
#         """)
#         self.btn_discard.clicked.connect(self.discard_image)
#         self.controls_layout.addWidget(self.btn_discard)
        
#         # Proceed (Thematic Gradient Action)
#         self.btn_proceed = QPushButton("Proceed")
#         self.btn_proceed.setEnabled(False)
#         self.btn_proceed.setStyleSheet(btn_style + """
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
        
#         # Operation Status Notification Label
#         self.status_label = QLabel("")
#         self.status_label.setStyleSheet("""
#             font-family: 'Poppins', sans-serif;
#             color: #10B981; /* Soft Green */
#             font-size: 13px; 
#             font-weight: bold;
#             background: transparent;
#         """)
#         self.main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
#         # Thread Initialization
#         self.camera_thread = CameraThread()
#         self.camera_thread.change_pixmap_signal.connect(self.update_frame)
#         self.camera_thread.start()

#     def back_to_dashboard(self):
#         self.camera_thread.stop()
#         # self.timer.stop()
#         subprocess.Popen([sys.executable, "loader.py"])
#         subprocess.Popen([sys.executable, "analysis_page1.py"])
#         self.close()

#     def proceed_next(self):
#         self.camera_thread.stop()
#         # self.timer.stop()
#         subprocess.Popen([sys.executable, "loader_large.py"])
#         subprocess.Popen([sys.executable, "analysis_page3.py"])
#         self.close()

#     def on_slider_zoom_changed(self, value):
#         factor = value / 10.0
#         self.zoom_label.setText(f"Zoom: {factor:.1f}x")
#         self.camera_view.set_zoom(factor)

#     def on_view_zoom_changed(self, factor):
#         # Keeps view trackbars synchronized with manual wheel events
#         self.zoom_slider.blockSignals(True)
#         self.zoom_slider.setValue(int(factor * 10))
#         self.zoom_slider.blockSignals(False)
#         self.zoom_label.setText(f"Zoom: {factor:.1f}x")

#     def update_frame(self, q_image, cropped_bgr):
#         if cropped_bgr is not None and not q_image.isNull():
#             self.current_frame = cropped_bgr
#             self.camera_view.set_image(q_image)
#             self.camera_view.setStyleSheet("""
#                 QGraphicsView {
#                     border: 2.5px dashed rgba(109, 40, 217, 0.22); 
#                     background-color: #000000; 
#                     border-radius: 16px;
#                 }
#             """)
#         else:
#             self.camera_view.set_image(QImage())
#             self.camera_view.setStyleSheet("""
#                 QGraphicsView {
#                     border: 2px dashed rgba(239, 68, 68, 0.3); 
#                     background-color: #000000; 
#                     border-radius: 16px;
#                 }
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
#             # Map coordinates to grab zoomed visible sub-region of raw dimensions
#             h, w, ch = self.current_frame.shape
#             roi = self.camera_view.get_visible_roi(w, h)
            
#             if roi is not None:
#                 rx_min, ry_min, rx_max, ry_max = roi
#                 # Extract panned and zoomed-in sub-portion
#                 frame_to_save = self.current_frame[ry_min:ry_max, rx_min:rx_max]
#             else:
#                 frame_to_save = self.current_frame
                
#             if frame_to_save.size == 0:
#                 frame_to_save = self.current_frame

#             # Saves the cropped high quality frame portion
#             cv2.imwrite(filepath, frame_to_save)
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

#     def closeEvent(self, event):
#         self.camera_thread.stop()
#         event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = CameraWindow()
#     window.showFullScreen()
#     window.show()
#     sys.exit(app.exec())
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"
import sys
# import os
import subprocess
import time
import numpy as np  # Imported for structural memory operations and color space math
import cv2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QGraphicsDropShadowEffect,
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider)
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal, QRectF
from PyQt6.QtGui import QImage, QPixmap, QColor, QPainter

class CameraThread(QThread):
    # Emits the enhanced GUI-display QImage and the pristine BGR frame for saving
    change_pixmap_signal = pyqtSignal(QImage, object)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        # Cache the CLAHE object to avoid re-creation overhead in the processing loop
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def run(self):
        # 1. Raspberry Pi Picamera2 stack
        try:
            from picamera2 import Picamera2
            picam = Picamera2()
            # Request RGB888 format configuration
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
                    
                    # --- HIGH-RESOLUTION PREVIEW PIPELINE ---
                    # Keep full cropped resolution for maximum detail retention
                    preview_rgb = cropped_rgb.copy()
                    
                    # Dynamic Illumination Boost (CLAHE in LAB color space)
                    lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    cl = self.clahe.apply(l)
                    enhanced_lab = cv2.merge((cl, a, b))
                    preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
                    # Gentle Sharpening (Clinical/Diagnostic grading visual enhancement)
                    sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
                    preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
                    # Final alignment and memory layout stride check
                    preview_rgb = np.ascontiguousarray(preview_rgb)
                    bytes_per_line = preview_rgb.strides[0]
                    
                    q_image = QImage(
                        preview_rgb.data, crop_size, crop_size, bytes_per_line, QImage.Format.Format_RGB888
                    ).copy()
                    
                    self.change_pixmap_signal.emit(q_image, cropped_bgr)
                self.msleep(33)
                
            picam.stop()
            picam.close()

        # 2. Fallback OpenCV VideoCapture
        except ImportError:
            cap = cv2.VideoCapture(0,cv2.CAP_V4L2)
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
                    
                    # --- HIGH-RESOLUTION PREVIEW PIPELINE ---
                    preview_rgb = cropped_rgb.copy()
                    
                    # Dynamic Illumination Boost (CLAHE in LAB space for natural, vivid color)
                    lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    cl = self.clahe.apply(l)
                    enhanced_lab = cv2.merge((cl, a, b))
                    preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
                    # Gentle Sharpening
                    sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
                    preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
                    # Explicit contiguous check and exact memory stride matching
                    preview_rgb = np.ascontiguousarray(preview_rgb)
                    bytes_per_line = preview_rgb.strides[0]
                    
                    q_image = QImage(
                        preview_rgb.data, crop_size, crop_size, bytes_per_line, QImage.Format.Format_RGB888
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
        # Enable high-quality bilinear filtering for the pixmap rendering
        self.pixmap_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.scene.addItem(self.pixmap_item)
        
        # Enable dragging/panning via touchscreen or mouse drag
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Apply high-quality rendering hints to the viewport
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        
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
        self.scene.setSceneRect(QRectF(pixmap.rect()))
        
        # Dynamically scale the image to fit the viewport based on current zoom
        self.update_view_transform()

    def update_view_transform(self):
        if self.pixmap_item.pixmap().isNull():
            return
            
        rect = self.pixmap_item.boundingRect()
        view_rect = self.viewport().rect()
        
        if rect.width() <= 0 or rect.height() <= 0 or view_rect.width() <= 0 or view_rect.height() <= 0:
            return
            
        # Calculate base scale factor to fit the high-resolution frame inside the display window
        scale_x = view_rect.width() / rect.width()
        scale_y = view_rect.height() / rect.height()
        fit_scale = min(scale_x, scale_y)
        
        # Combine the viewport-fit scale with the user's zoom factor
        total_scale = fit_scale * self.zoom_factor
        
        self.resetTransform()
        self.scale(total_scale, total_scale)

    def set_zoom(self, value):
        self.zoom_factor = max(1.0, min(value, 10.0))
        self.update_view_transform()
        self.zoom_changed.emit(self.zoom_factor)

    def wheelEvent(self, event):
        # Support zooming through physical scroll-wheels
        zoom_step = 1.15 if event.angleDelta().y() > 0 else 0.85
        new_zoom = self.zoom_factor * zoom_step
        self.set_zoom(new_zoom)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_view_transform()

    def get_visible_roi(self, original_width, original_height):
        """
        Maps viewport coordinates back to original image coordinates 
        to isolate the cropped zoom sector.
        """
        if self.pixmap_item.pixmap().isNull():
            return None
            
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
        self.zoom_slider.setMinimum(10)  # Representing 1.0x
        self.zoom_slider.setMaximum(100)  # Representing 10.0x
        self.zoom_slider.setRange(10, 100)  # Maps from 1.0x (10) to 10.0x (100)
        self.zoom_slider.setValue(10)
        self.zoom_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 2px solid rgba(109, 40, 217, 0.2);
                height: 14px;
                background: rgba(109, 40, 217, 0.1);
                border-radius: 6px;
            }
            QSlider::handle:horizontal {
                background: #6D28D9;
                border: 1px solid #5B21B6;
                width: 28px;
                height: 28px;
                margin: -5px 0;
                border-radius: 14px;
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
        subprocess.Popen([sys.executable, "loader.py"])
        subprocess.Popen([sys.executable, "analysis_page1.py"])
        self.close()

    def proceed_next(self):
        self.camera_thread.stop()
        subprocess.Popen([sys.executable, "loader_large.py"])
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
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())