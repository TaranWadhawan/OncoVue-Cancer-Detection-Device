import sys
import os
import time
import subprocess
import numpy as np
import cv2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QGraphicsDropShadowEffect,
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSlider)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QRectF
from PyQt6.QtGui import QImage, QPixmap, QColor

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage, object)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        try:
            from picamera2 import Picamera2
            picam = Picamera2()
            config = picam.create_preview_configuration(
                main={"size": (4056, 3040), "format": "RGB888"}
            )
            picam.configure(config)
            picam.start()
            
            self.msleep(600)
            
            while self._run_flag:
                frame = picam.capture_array() 
                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    h, w, ch = frame.shape
                    
                    crop_size = min(2500, h, w)
                    start_y = (h - crop_size) // 2
                    start_x = (w - crop_size) // 2
                    
                    cropped_rgb = np.ascontiguousarray(
                        frame[start_y:start_y+crop_size, start_x:start_x+crop_size]
                    )
                    cropped_bgr = cv2.cvtColor(cropped_rgb, cv2.COLOR_RGB2BGR)
                    
                    preview_size = 800
                    preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
                    lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cl = clahe.apply(l)
                    enhanced_lab = cv2.merge((cl, a, b))
                    preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
                    sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
                    preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
                    preview_rgb = np.ascontiguousarray(preview_rgb)
                    bytes_per_line = preview_rgb.strides[0]
                    
                    q_image = QImage(
                        preview_rgb.data, preview_size, preview_size, bytes_per_line, QImage.Format.Format_RGB888
                    ).copy()
                    
                    self.change_pixmap_signal.emit(q_image, cropped_bgr)
                self.msleep(33)
                
            picam.stop()
            picam.close()

        except Exception:
            pipeline = "libcamerasrc ! video/x-raw, width=4056, height=3040, framerate=10/1 ! videoconvert ! appsink"
            cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
            
            if not cap or not cap.isOpened():
                cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4056)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3040)
            
            for _ in range(15):
                cap.read()
            
            while self._run_flag:
                ret, frame = cap.read()
                if ret:
                    h, w, ch = frame.shape
                    
                    crop_size = min(2500, h, w)
                    start_y = (h - crop_size) // 2
                    start_x = (w - crop_size) // 2
                    
                    cropped_bgr = np.ascontiguousarray(
                        frame[start_y:start_y+crop_size, start_x:start_x+crop_size]
                    )
                    cropped_rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)
                    
                    preview_size = 800
                    preview_rgb = cv2.resize(cropped_rgb, (preview_size, preview_size), interpolation=cv2.INTER_AREA)
                    
                    lab = cv2.cvtColor(preview_rgb, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cl = clahe.apply(l)
                    enhanced_lab = cv2.merge((cl, a, b))
                    preview_rgb = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
                    
                    sharpen_kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
                    preview_rgb = cv2.filter2D(preview_rgb, -1, sharpen_kernel)
                    
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
    zoom_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.zoom_factor = 1.0
        
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

    def set_zoom(self, value):
        self.zoom_factor = max(1.0, min(value, 10.0))
        self.resetTransform()
        self.scale(self.zoom_factor, self.zoom_factor)
        self.zoom_changed.emit(self.zoom_factor)

    def wheelEvent(self, event):
        zoom_step = 1.15 if event.angleDelta().y() > 0 else 0.85
        new_zoom = self.zoom_factor * zoom_step
        self.set_zoom(new_zoom)

    def get_visible_roi(self, original_width, original_height):
        if self.pixmap_item.pixmap().isNull():
            return None
            
        viewport_rect = self.viewport().rect()
        scene_rect = self.mapToScene(viewport_rect).boundingRect()
        
        img_rect = self.pixmap_item.boundingRect()
        if img_rect.width() <= 0 or img_rect.height() <= 0:
            return None
            
        x_min = max(0.0, scene_rect.left())
        y_min = max(0.0, scene_rect.top())
        x_max = min(img_rect.width(), scene_rect.right())
        y_max = min(img_rect.height(), scene_rect.bottom())
        
        scale_x = original_width / img_rect.width()
        scale_y = original_height / img_rect.height()
        
        rx_min = int(x_min * scale_x)
        ry_min = int(y_min * scale_y)
        rx_max = int(x_max * scale_x)
        ry_max = int(y_max * scale_y)
        
        return rx_min, ry_min, rx_max, ry_max

class DatasetCaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OncoVue - Dataset Capture Tool")
        self.setFixedSize(1280, 720)
        
        self.dataset_dir = "dataset"
        self.classes = ["her0", "her1", "her2", "her3"]
        self.init_dataset_folders()
        
        self.last_captured_path = None
        self.current_frame = None
        
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
        self.main_layout.setSpacing(10)
        
        self.top_bar = QHBoxLayout()
        self.btn_back = QPushButton("← Back")
        self.btn_back.setFixedSize(110, 38)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: rgba(109, 40, 217, 0.08);
                border: 1px solid rgba(109, 40, 217, 0.18);
                color: #4C1D95;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(109, 40, 217, 0.15);
                border-color: rgba(109, 40, 217, 0.3);
            }
        """)
        self.btn_back.clicked.connect(self.back_to_dashboard)
        self.top_bar.addWidget(self.btn_back)
        self.top_bar.addStretch()
        self.main_layout.addLayout(self.top_bar)
        
        self.camera_view = ZoomableGraphicsView()
        self.camera_view.setFixedSize(500, 500)
        
        shadow_cam = QGraphicsDropShadowEffect(self)
        shadow_cam.setBlurRadius(35)
        shadow_cam.setColor(QColor(109, 40, 217, 25))
        shadow_cam.setOffset(0, 8)
        self.camera_view.setGraphicsEffect(shadow_cam)
        
        self.main_layout.addWidget(self.camera_view, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.zoom_layout = QHBoxLayout()
        self.zoom_layout.setSpacing(10)
        self.zoom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.zoom_label = QLabel("Zoom: 1.0x")
        self.zoom_label.setStyleSheet("font-family: 'Poppins', sans-serif; color: #4C1D95; font-size: 13px; font-weight: bold;")
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setFixedWidth(300)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(100)
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
        
        self.controls_layout = QHBoxLayout()
        self.controls_layout.setSpacing(10)
        self.controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.controls_layout)
        
        btn_style = """
            QPushButton {
                font-family: 'Poppins', 'Inter', sans-serif;
                font-weight: bold;
                font-size: 13px;
                border: none;
                border-radius: 6px;
                padding: 10px 15px;
                color: white;
                min-width: 110px;
            }
        """
        
        self.btn_her0 = QPushButton("Capture Her0")
        self.btn_her0.setStyleSheet(btn_style + "QPushButton{background-color: #9b59b6;} QPushButton:hover{background-color: #8e44ad;}")
        self.btn_her0.clicked.connect(lambda: self.capture_as_class("her0"))
        self.controls_layout.addWidget(self.btn_her0)
        
        self.btn_her1 = QPushButton("Capture Her1")
        self.btn_her1.setStyleSheet(btn_style + "QPushButton{background-color: #3498db;} QPushButton:hover{background-color: #2980b9;}")
        self.btn_her1.clicked.connect(lambda: self.capture_as_class("her1"))
        self.controls_layout.addWidget(self.btn_her1)
        
        self.btn_her2 = QPushButton("Capture Her2")
        self.btn_her2.setStyleSheet(btn_style + "QPushButton{background-color: #e67e22;} QPushButton:hover{background-color: #d35400;}")
        self.btn_her2.clicked.connect(lambda: self.capture_as_class("her2"))
        self.controls_layout.addWidget(self.btn_her2)
        
        self.btn_her3 = QPushButton("Capture Her3")
        self.btn_her3.setStyleSheet(btn_style + "QPushButton{background-color: #e74c3c;} QPushButton:hover{background-color: #c0392b;}")
        self.btn_her3.clicked.connect(lambda: self.capture_as_class("her3"))
        self.controls_layout.addWidget(self.btn_her3)
        
        self.btn_discard = QPushButton("Discard")
        self.btn_discard.setEnabled(False)
        self.btn_discard.setStyleSheet(btn_style + "QPushButton{background-color: #7f8c8d;} QPushButton:hover{background-color: #6a7475;} QPushButton:disabled{background-color: rgba(109, 40, 217, 0.08); color: rgba(109, 40, 217, 0.35);}")
        self.btn_discard.clicked.connect(self.discard_image)
        self.controls_layout.addWidget(self.btn_discard)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-family: 'Poppins', sans-serif; color: #10B981; font-size: 13px; font-weight: bold; background: transparent;")
        self.main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_frame)
        self.camera_thread.start()

    def back_to_dashboard(self):
        self.camera_thread.stop()
        subprocess.Popen([sys.executable, "page3.py"])
        self.close()

    def init_dataset_folders(self):
        os.makedirs(self.dataset_dir, exist_ok=True)
        for c in self.classes:
            os.makedirs(os.path.join(self.dataset_dir, c), exist_ok=True)

    def on_slider_zoom_changed(self, value):
        factor = value / 10.0
        self.zoom_label.setText(f"Zoom: {factor:.1f}x")
        self.camera_view.set_zoom(factor)

    def on_view_zoom_changed(self, factor):
        self.zoom_slider.blockSignals(True)
        self.zoom_slider.setValue(int(factor * 10))
        self.zoom_slider.blockSignals(False)
        self.zoom_label.setText(f"Zoom: {factor:.1f}x")

    def update_frame(self, q_image, cropped_bgr):
        if cropped_bgr is not None and not q_image.isNull():
            self.current_frame = cropped_bgr
            self.camera_view.set_image(q_image)

    def capture_as_class(self, class_name):
        self.status_label.setStyleSheet("color: #10B981; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
        self.status_label.clear()
        
        if self.current_frame is None:
            self.status_label.setStyleSheet("color: #EF4444; font-family: 'Poppins', sans-serif; font-size: 13px; font-weight: bold;")
            self.status_label.setText("Error: No live frame to capture.")
            return
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"img_{timestamp}.png"
        filepath = os.path.join(self.dataset_dir, class_name, filename)
        
        try:
            h, w, ch = self.current_frame.shape
            roi = self.camera_view.get_visible_roi(w, h)
            
            if roi is not None:
                rx_min, ry_min, rx_max, ry_max = roi
                frame_to_save = self.current_frame[ry_min:ry_max, rx_min:rx_max]
            else:
                frame_to_save = self.current_frame
                
            if frame_to_save.size == 0:
                frame_to_save = self.current_frame

            cv2.imwrite(filepath, frame_to_save)
            self.last_captured_path = filepath
            self.btn_discard.setEnabled(True)
            self.status_label.setText(f"Success: Saved to {filepath}")
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
    window = DatasetCaptureWindow()
    # window.showFullScreen()
    window.show()
    sys.exit(app.exec())