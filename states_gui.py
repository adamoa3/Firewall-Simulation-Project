from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

class TimeoutWindow(QDialog):
    def __init__(self, current_default):
        super().__init__()
        self.setWindowTitle("Change Default Timeout")
        self.default = current_default

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.timeout = QLineEdit()
        layout.addWidget(QLabel("Enter desired timeout: (new states will expire after this many seconds)"))
        layout.addWidget(self.timeout)

        layout.addSpacing(20)

        button_layout = QHBoxLayout()

        add_button = QPushButton("Change")
        add_button.clicked.connect(self.accept)
        button_layout.addWidget(add_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def get_time(self):
        return self.get_int(self.timeout.text())

    # will return number if valid as int, or current default otherwise
    def get_int(self, value):
        value = value.strip()
        if value.isdigit():
            return int(value)
        else:
            return self.default






