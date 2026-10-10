
# # import sys
# # import types
# # from PyQt6.QtWidgets import QDialog, QGridLayout, QPushButton, QApplication, QLineEdit, QTextEdit
# # from PyQt6.QtCore import Qt, QPoint

# # class VirtualKeyboard(QDialog):
# #     def __init__(self, parent=None):
# #         super().__init__(parent)
# #         self.setWindowFlags(
# #             Qt.WindowType.Tool | 
# #             Qt.WindowType.FramelessWindowHint | 
# #             Qt.WindowType.WindowStaysOnTopHint | 
# #             Qt.WindowType.WindowDoesNotAcceptFocus
# #         )
# #         self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
# #         self.setFixedSize(460, 260)
# #         self.setStyleSheet("background-color: #34495e; border: 2px solid #7f8c8d; border-radius: 8px;")
# #         self.drag_position = QPoint()
        
# #         self.grid_layout = QGridLayout(self)
# #         self.grid_layout.setContentsMargins(5, 5, 5, 5)
# #         self.grid_layout.setSpacing(3)
        
# #         keys = [
# #             ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Back'],
# #             ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '@'],
# #             ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '.', '_'],
# #             ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'Space', 'Enter']
# #         ]
        
# #         for row_idx, row in enumerate(keys):
# #             for col_idx, char in enumerate(row):
# #                 btn = QPushButton(char)
# #                 btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
# #                 btn.setStyleSheet("""
# #                     QPushButton {
# #                         background-color: #2c3e50;
# #                         color: white;
# #                         border: none;
# #                         border-radius: 4px;
# #                         font-size: 14px;
# #                         font-weight: bold;
# #                     }
# #                     QPushButton:hover {
# #                         background-color: #1a252f;
# #                     }
# #                 """)
                
# #                 colspan = 1
# #                 if char == 'Space':
# #                     colspan = 2
# #                     btn.clicked.connect(lambda checked, c=' ': self.key_clicked(c))
# #                 elif char == 'Back':
# #                     btn.clicked.connect(self.backspace_clicked)
# #                 elif char == 'Enter':
# #                     colspan = 2
# #                     btn.clicked.connect(self.enter_clicked)
# #                 else:
# #                     btn.clicked.connect(lambda checked, c=char: self.key_clicked(c))
                    
# #                 self.grid_layout.addWidget(btn, row_idx, col_idx, 1, colspan)

# #     def get_active_input(self):
# #         widget = QApplication.focusWidget()
# #         if widget and (isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit)):
# #             return widget
            
# #         for w in QApplication.topLevelWidgets():
# #             if w.isActiveWindow():
# #                 for child in w.findChildren((QLineEdit, QTextEdit)):
# #                     if child.hasFocus():
# #                         return child
# #         return None

# #     def key_clicked(self, char):
# #         widget = self.get_active_input()
# #         if widget and hasattr(widget, 'insert'):
# #             widget.insert(char)

# #     def backspace_clicked(self):
# #         widget = self.get_active_input()
# #         if not widget:
# #             return
            
# #         if isinstance(widget, QLineEdit):
# #             widget.backspace()
# #         elif isinstance(widget, QTextEdit):
# #             cursor = widget.textCursor()
# #             cursor.deletePreviousChar()
# #             widget.setTextCursor(cursor)

# #     def enter_clicked(self):
# #         widget = self.get_active_input()
# #         if not widget:
# #             return
            
# #         if isinstance(widget, QLineEdit):
# #             widget.returnPressed.emit()
# #         elif isinstance(widget, QTextEdit):
# #             widget.insert('\n')

# #     def mousePressEvent(self, event):
# #         if event.button() == Qt.MouseButton.LeftButton:
# #             self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
# #             event.accept()

# #     def mouseMoveEvent(self, event):
# #         if event.buttons() == Qt.MouseButton.LeftButton:
# #             self.move(event.globalPosition().toPoint() - self.drag_position)
# #             event.accept()


# import sys
# import types
# from PyQt6.QtWidgets import QDialog, QGridLayout, QPushButton, QApplication, QLineEdit, QTextEdit, QGraphicsDropShadowEffect
# from PyQt6.QtCore import Qt, QPoint
# from PyQt6.QtGui import QColor

# class VirtualKeyboard(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowFlags(
#             Qt.WindowType.Tool | 
#             Qt.WindowType.FramelessWindowHint | 
#             Qt.WindowType.WindowStaysOnTopHint | 
#             Qt.WindowType.WindowDoesNotAcceptFocus
#         )
#         self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
#         self.setFixedSize(460, 320)
        
#         # Frosted Dark Indigo Slate shell
#         self.setStyleSheet("""
#             background-color: rgba(30, 27, 75, 0.9); 
#             border: 2px solid rgba(168, 85, 247, 0.25); 
#             border-radius: 12px;
#         """)
        
#         # Soft outer purple bloom shadow
#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(35)
#         shadow.setColor(QColor(109, 40, 217, 35))
#         shadow.setOffset(0, 8)
#         self.setGraphicsEffect(shadow)
        
#         self.drag_position = QPoint()
#         self.shift_active = False
#         self.char_buttons = {}
        
#         self.grid_layout = QGridLayout(self)
#         self.grid_layout.setContentsMargins(12, 12, 12, 12)
#         self.grid_layout.setSpacing(5)
        
#         # Translucent glass keys with Poppins typography matching the dark theme
#         self.btn_style = """
#             QPushButton {
#                 background-color: rgba(255, 255, 255, 0.08);
#                 border: 1px solid rgba(168, 85, 247, 0.15);
#                 color: #FAF7FF; /* Frost White */
#                 border-radius: 6px;
#                 font-family: 'Poppins', 'Inter', sans-serif;
#                 font-size: 14px;
#                 font-weight: bold;
#                 min-height: 48px;
#             }
#             QPushButton:hover {
#                 background-color: rgba(168, 85, 247, 0.22);
#                 border-color: rgba(168, 85, 247, 0.4);
#             }
#         """
#         self.setup_keyboard()

#     def setup_keyboard(self):
#         layout_matrix = [
#             [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("0", "0"), ("Back", "Back")],
#             [("q", "Q"), ("w", "W"), ("e", "E"), ("r", "R"), ("t", "T"), ("y", "Y"), ("u", "U"), ("i", "I"), ("o", "O"), ("p", "P"), ("@", "@")],
#             [("a", "A"), ("s", "S"), ("d", "D"), ("f", "F"), ("g", "G"), ("h", "H"), ("j", "J"), ("k", "K"), ("l", "L"), (".", "."), ("_", "_")],
#             [("Shift", "Shift"), ("z", "Z"), ("x", "X"), ("c", "C"), ("v", "V"), ("b", "B"), ("n", "N"), ("m", "M"), (",", ","), ("?", "?"), ("/", "/")],
#             [("Space", "Space"), ("Enter", "Enter")]
#         ]
        
#         for row_idx, row in enumerate(layout_matrix):
#             for col_idx, (lower, upper) in enumerate(row):
#                 if lower == "Space":
#                     btn = QPushButton("Space")
#                     btn.setStyleSheet(self.btn_style + """
#                         QPushButton {
#                             background-color: rgba(255, 255, 255, 0.04); 
#                             border: 1px solid rgba(168, 85, 247, 0.12);
#                         }
#                     """)
#                     btn.clicked.connect(lambda checked: self.key_clicked(" "))
#                     self.grid_layout.addWidget(btn, row_idx, 0, 1, 7)
#                 elif lower == "Enter":
#                     btn = QPushButton("Enter")
#                     btn.setStyleSheet(self.btn_style + """
#                         QPushButton {
#                             background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                                 stop:0 #EC4899, 
#                                 stop:1 #6D28D9); /* Rose to Orchid gradient */
#                             border: none;
#                         }
#                         QPushButton:hover {
#                             background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
#                                 stop:0 #F472B6, 
#                                 stop:1 #7C3AED);
#                         }
#                     """)
#                     btn.clicked.connect(self.enter_clicked)
#                     self.grid_layout.addWidget(btn, row_idx, 7, 1, 4)
#                 else:
#                     btn = QPushButton(lower)
#                     btn.setStyleSheet(self.btn_style)
                    
#                     if lower == "Back":
#                         btn.setStyleSheet(self.btn_style + """
#                             QPushButton {
#                                 background-color: #EF4444; /* Soft Crimson */
#                                 border: none;
#                             }
#                             QPushButton:hover {
#                                 background-color: #DC2626;
#                             }
#                         """)
#                         btn.clicked.connect(self.backspace_clicked)
#                     elif lower == "Shift":
#                         btn.setStyleSheet(self.btn_style + """
#                             QPushButton {
#                                 background-color: #6D28D9; /* Orchid Purple */
#                                 border: none;
#                             }
#                             QPushButton:hover {
#                                 background-color: #7C3AED;
#                             }
#                         """)
#                         btn.clicked.connect(self.toggle_shift)
#                     else:
#                         self.char_buttons[btn] = (lower, upper)
#                         btn.clicked.connect(lambda checked, b=btn: self.char_clicked(b))
                        
#                     btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
#                     self.grid_layout.addWidget(btn, row_idx, col_idx, 1, 1)

#     def toggle_shift(self):
#         self.shift_active = not self.shift_active
#         for btn, (lower, upper) in self.char_buttons.items():
#             btn.setText(upper if self.shift_active else lower)
            
#         sender = self.sender()
#         if sender:
#             if self.shift_active:
#                 # Toggle active Shift to glowing Rose Pink state
#                 sender.setStyleSheet(self.btn_style + """
#                     QPushButton {
#                         background-color: #EC4899; 
#                         border: 1.5px solid #FAF7FF;
#                     }
#                     QPushButton:hover {
#                         background-color: #F472B6;
#                     }
#                 """)
#             else:
#                 sender.setStyleSheet(self.btn_style + """
#                     QPushButton {
#                         background-color: #6D28D9; 
#                         border: none;
#                     }
#                     QPushButton:hover {
#                         background-color: #7C3AED;
#                     }
#                 """)

#     def char_clicked(self, btn):
#         lower, upper = self.char_buttons[btn]
#         char = upper if self.shift_active else lower
#         self.key_clicked(char)

#     def get_active_input(self):
#         widget = QApplication.focusWidget()
#         if widget and (isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit)):
#             return widget
            
#         for w in QApplication.topLevelWidgets():
#             if w.isActiveWindow():
#                 for child in w.findChildren((QLineEdit, QTextEdit)):
#                     if child.hasFocus():
#                         return child
#         return None

#     def key_clicked(self, char):
#         widget = self.get_active_input()
#         if widget and hasattr(widget, 'insert'):
#             widget.insert(char)

#     def backspace_clicked(self):
#         widget = self.get_active_input()
#         if not widget:
#             return
            
#         if isinstance(widget, QLineEdit):
#             widget.backspace()
#         elif isinstance(widget, QTextEdit):
#             cursor = widget.textCursor()
#             cursor.deletePreviousChar()
#             widget.setTextCursor(cursor)

#     def enter_clicked(self):
#         widget = self.get_active_input()
#         if not widget:
#             return
            
#         if isinstance(widget, QLineEdit):
#             widget.returnPressed.emit()
#         elif isinstance(widget, QTextEdit):
#             widget.insert('\n')

#     def mousePressEvent(self, event):
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
#             event.accept()

#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.MouseButton.LeftButton:
#             self.move(event.globalPosition().toPoint() - self.drag_position)
#             event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     keyboard = VirtualKeyboard()
#     keyboard.show()
#     sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import (
    QDialog, QGridLayout, QPushButton, QApplication, QLineEdit, QTextEdit, 
    QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor

class VirtualKeyboard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Tool | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        
        # Sizing configurations
        self.expanded_size = (540, 380)
        self.collapsed_size = (50, 50)
        self.is_minimized = False
        
        self.setFixedSize(*self.expanded_size)
        
        # Soft outer purple bloom shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(35)
        self.shadow.setColor(QColor(109, 40, 217, 35))
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)
        
        self.drag_position = QPoint()
        self.drag_started = False
        self.shift_active = False
        self.char_buttons = {}
        
        # Main structure
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.btn_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(168, 85, 247, 0.15);
                color: #FAF7FF; /* Frost White */
                border-radius: 6px;
                font-family: 'Poppins', 'Inter', sans-serif;
                font-size: 16px;
                font-weight: bold;
                min-height: 56px;
            }
            QPushButton:hover {
                background-color: rgba(168, 85, 247, 0.22);
                border-color: rgba(168, 85, 247, 0.4);
            }
        """
        
        self.setup_ui()
        self.apply_theme()

    def apply_theme(self):
        if self.is_minimized:
            # Minimalist floating orb styling
            self.setStyleSheet("""
                QDialog {
                    background-color: rgba(109, 40, 217, 0.85); /* Radiant orchid base */
                    border: 2px solid rgba(236, 72, 153, 0.6);   /* Glowing pink border */
                    border-radius: 25px; /* Circular for 50x50 size */
                }
            """)
        else:
            # Classic Frosted Dark Indigo Slate shell
            self.setStyleSheet("""
                QDialog {
                    background-color: rgba(30, 27, 75, 0.9); 
                    border: 2px solid rgba(168, 85, 247, 0.25); 
                    border-radius: 12px;
                }
            """)

    def setup_ui(self):
        # 1. Header Area with the small control circle
        self.header_widget = QWidget()
        self.header_widget.setFixedHeight(30)
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(12, 8, 12, 0)
        
        # Spacer to push the control button to the right side
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Minimalist control circle
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(14, 14)
        self.toggle_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #EC4899; /* Bright Rose */
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #F472B6; /* Soft light-up pink */
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_minimize)
        header_layout.addWidget(self.toggle_btn)
        
        self.main_layout.addWidget(self.header_widget)

        # 2. Keyboard Keys Container
        self.keyboard_widget = QWidget()
        self.grid_layout = QGridLayout(self.keyboard_widget)
        self.grid_layout.setContentsMargins(12, 4, 12, 12)
        self.grid_layout.setSpacing(5)
        
        self.setup_keyboard()
        self.main_layout.addWidget(self.keyboard_widget)

    def setup_keyboard(self):
        layout_matrix = [
            [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("0", "0"), ("Back", "Back")],
            [("q", "Q"), ("w", "W"), ("e", "E"), ("r", "R"), ("t", "T"), ("y", "Y"), ("u", "U"), ("i", "I"), ("o", "O"), ("p", "P"), ("@", "@")],
            [("a", "A"), ("s", "S"), ("d", "D"), ("f", "F"), ("g", "G"), ("h", "H"), ("j", "J"), ("k", "K"), ("l", "L"), (".", "."), ("_", "_")],
            [("Shift", "Shift"), ("z", "Z"), ("x", "X"), ("c", "C"), ("v", "V"), ("b", "B"), ("n", "N"), ("m", "M"), (",", ","), ("?", "?"), ("/", "/")],
            [("Space", "Space"), ("Enter", "Enter")]
        ]
        
        for row_idx, row in enumerate(layout_matrix):
            for col_idx, (lower, upper) in enumerate(row):
                if lower == "Space":
                    btn = QPushButton("Space")
                    btn.setStyleSheet(self.btn_style + """
                        QPushButton {
                            background-color: rgba(255, 255, 255, 0.04); 
                            border: 1px solid rgba(168, 85, 247, 0.12);
                        }
                    """)
                    btn.clicked.connect(lambda checked: self.key_clicked(" "))
                    self.grid_layout.addWidget(btn, row_idx, 0, 1, 7)
                elif lower == "Enter":
                    btn = QPushButton("Enter")
                    btn.setStyleSheet(self.btn_style + """
                        QPushButton {
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                stop:0 #EC4899, 
                                stop:1 #6D28D9); /* Rose to Orchid gradient */
                            border: none;
                        }
                        QPushButton:hover {
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                stop:0 #F472B6, 
                                stop:1 #7C3AED);
                        }
                    """)
                    btn.clicked.connect(self.enter_clicked)
                    self.grid_layout.addWidget(btn, row_idx, 7, 1, 4)
                else:
                    btn = QPushButton(lower)
                    btn.setStyleSheet(self.btn_style)
                    
                    if lower == "Back":
                        btn.setStyleSheet(self.btn_style + """
                            QPushButton {
                                background-color: #EF4444; /* Soft Crimson */
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #DC2626;
                            }
                        """)
                        btn.clicked.connect(self.backspace_clicked)
                    elif lower == "Shift":
                        btn.setStyleSheet(self.btn_style + """
                            QPushButton {
                                background-color: #6D28D9; /* Orchid Purple */
                                border: none;
                            }
                            QPushButton:hover {
                                background-color: #7C3AED;
                            }
                        """)
                        btn.clicked.connect(self.toggle_shift)
                    else:
                        self.char_buttons[btn] = (lower, upper)
                        btn.clicked.connect(lambda checked, b=btn: self.char_clicked(b))
                        
                    btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    self.grid_layout.addWidget(btn, row_idx, col_idx, 1, 1)

    def toggle_minimize(self):
        self.is_minimized = not self.is_minimized
        
        if self.is_minimized:
            # Hide layout parts
            self.keyboard_widget.hide()
            self.header_widget.hide()
            # Convert size to a small floating orb
            self.setFixedSize(*self.collapsed_size)
        else:
            # Expand back to normal layout
            self.setFixedSize(*self.expanded_size)
            self.keyboard_widget.show()
            self.header_widget.show()
            
        self.apply_theme()

    def toggle_shift(self):
        self.shift_active = not self.shift_active
        for btn, (lower, upper) in self.char_buttons.items():
            btn.setText(upper if self.shift_active else lower)
            
        sender = self.sender()
        if sender:
            if self.shift_active:
                sender.setStyleSheet(self.btn_style + """
                    QPushButton {
                        background-color: #EC4899; 
                        border: 1.5px solid #FAF7FF;
                    }
                    QPushButton:hover {
                        background-color: #F472B6;
                    }
                """)
            else:
                sender.setStyleSheet(self.btn_style + """
                    QPushButton {
                        background-color: #6D28D9; 
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #7C3AED;
                    }
                """)

    def char_clicked(self, btn):
        lower, upper = self.char_buttons[btn]
        char = upper if self.shift_active else lower
        self.key_clicked(char)

    def get_active_input(self):
        widget = QApplication.focusWidget()
        if widget and (isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit)):
            return widget
            
        for w in QApplication.topLevelWidgets():
            if w.isActiveWindow():
                for child in w.findChildren((QLineEdit, QTextEdit)):
                    if child.hasFocus():
                        return child
        return None

    def key_clicked(self, char):
        widget = self.get_active_input()
        if widget and hasattr(widget, 'insert'):
            widget.insert(char)

    def backspace_clicked(self):
        widget = self.get_active_input()
        if not widget:
            return
            
        if isinstance(widget, QLineEdit):
            widget.backspace()
        elif isinstance(widget, QTextEdit):
            cursor = widget.textCursor()
            cursor.deletePreviousChar()
            widget.setTextCursor(cursor)

    def enter_clicked(self):
        widget = self.get_active_input()
        if not widget:
            return
            
        if isinstance(widget, QLineEdit):
            widget.returnPressed.emit()
        elif isinstance(widget, QTextEdit):
            widget.insert('\n')

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.drag_started = False
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.drag_started = True
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # If minimized and the user tapped the orb without dragging it, restore the keyboard
            if self.is_minimized and not self.drag_started:
                self.toggle_minimize()
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    keyboard = VirtualKeyboard()
    keyboard.show()
    sys.exit(app.exec())