import os
import sys
import numpy as np
from PIL import Image

# PyQt5 Imports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFileDialog, QWidget, QProgressBar)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# TFLite Imports
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except ImportError:
        print("Error: Please install tflite-runtime or tensorflow.")
        sys.exit(1)

# ==========================================
# CONFIGURATION
# ==========================================
MODEL_PATH = "model.lite"
# Replace these with your actual 4 classes in alphabetical order
LABELS = ["her_0", "her_1", "her_2", "her_3"] 
# ==========================================

class ImageClassifierGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        
        # Initialize UI and Load Model
        self.initUI()
        self.load_model()

    def initUI(self):
        self.setWindowTitle('Edge Impulse 4-Class Image Classifier')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        # Main Layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Left Side: Image Display and Load Button
        self.btn_load = QPushButton('Select Image', self)
        self.btn_load.setFont(QFont('Arial', 12, QFont.Bold))
        self.btn_load.setStyleSheet("background-color: #007acc; color: white; padding: 10px; border-radius: 5px;")
        self.btn_load.clicked.connect(self.open_image_dialog)
        left_layout.addWidget(self.btn_load)

        self.lbl_image = QLabel(self)
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setText("No Image Selected")
        self.lbl_image.setStyleSheet("border: 2px dashed #cccccc; background-color: #ffffff; min-width: 400px; min-height: 400px;")
        left_layout.addWidget(self.lbl_image)

        # Right Side: Results Display
        self.lbl_result_title = QLabel('Classification Results', self)
        self.lbl_result_title.setFont(QFont('Arial', 14, QFont.Bold))
        right_layout.addWidget(self.lbl_result_title)

        # Create progress bars and labels for the 4 classes
        self.class_labels = []
        self.progress_bars = []
        
        for i in range(len(LABELS)):
            lbl = QLabel(f"{LABELS[i]}: 0.0%", self)
            lbl.setFont(QFont('Arial', 11))
            right_layout.addWidget(lbl)
            self.class_labels.append(lbl)

            bar = QProgressBar(self)
            bar.setMaximum(100)
            bar.setValue(0)
            bar.setStyleSheet("QProgressBar::chunk { background-color: #4caf50; }")
            right_layout.addWidget(bar)
            self.progress_bars.append(bar)

        right_layout.addStretch()

        # Summary Label (Best prediction)
        self.lbl_summary = QLabel('Prediction: None', self)
        self.lbl_summary.setFont(QFont('Arial', 14, QFont.Bold))
        self.lbl_summary.setStyleSheet("color: #333333; padding: 10px; background-color: #e0e0e0; border-radius: 5px;")
        right_layout.addWidget(self.lbl_summary)

        # Set Main Layout
        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_model(self):
        """Loads the TFLite model in the background."""
        if not os.path.exists(MODEL_PATH):
            self.lbl_summary.setText("Error: model.tflite not found!")
            self.btn_load.setEnabled(False)
            return

        try:
            self.interpreter = tflite.Interpreter(model_path=MODEL_PATH)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        except Exception as e:
            self.lbl_summary.setText(f"Error loading model: {str(e)}")

    def open_image_dialog(self):
        """Opens a file dialog to pick an image."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image to Classify", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp)", 
            options=options
        )
        
        if file_path:
            self.display_image(file_path)
            self.classify_image(file_path)

    def display_image(self, file_path):
        """Displays the selected image in the GUI."""
        pixmap = QPixmap(file_path)
        # Scale image to fit the label, maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(self.lbl_image.width(), self.lbl_image.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl_image.setPixmap(scaled_pixmap)

    def preprocess_image(self, image_path, input_shape):
        """Preprocesses the image for the model."""
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
        """Runs inference and updates the GUI with results."""
        if not self.interpreter:
            return

        try:
            input_shape = self.input_details[0]['shape']
            input_data = self.preprocess_image(image_path, input_shape)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
            
            # Find max index
            max_idx = np.argmax(output_data)
            
            # Update Progress bars and Labels
            for i in range(len(LABELS)):
                score = output_data[i]
                percentage = int(score * 100)
                
                # Update text and progress bars
                self.class_labels[i].setText(f"{LABELS[i]}: {score*100:.1f}%")
                self.progress_bars[i].setValue(percentage)
            
            # Update Summary Label
            predicted_class = LABELS[max_idx]
            confidence = output_data[max_idx] * 100
            self.lbl_summary.setText(f"Prediction: {predicted_class} ({confidence:.1f}%)")

        except Exception as e:
            self.lbl_summary.setText(f"Error during classification: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageClassifierGUI()
    ex.show()
    sys.exit(app.exec_())