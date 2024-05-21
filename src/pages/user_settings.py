from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QAction
from qtawesome import icon

class PasswordLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.reveal_password_action = QAction(icon('fa5s.eye'), 'Reveal Password')
        self.reveal_password_action.triggered.connect(self.toggle_password_visibility)
        self.addAction(self.reveal_password_action, QLineEdit.ActionPosition.TrailingPosition)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.reveal_password_action.setVisible(False)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.reveal_password_action.setVisible(True)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.reveal_password_action.setVisible(False)
        self.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_password_visibility(self):
        if self.echoMode() == QLineEdit.EchoMode.Password:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)

class UserSettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.email_label = QLabel("Email")
        self.current_email = QLineEdit()
        self.new_email = QLineEdit()
        self.confirm_email = QLineEdit()
        self.change_email_btn = QPushButton("Change Email")
        self.password_label = QLabel("Password")
        self.current_password = PasswordLineEdit()
        self.new_password = PasswordLineEdit()
        self.confirm_password = PasswordLineEdit()
        self.change_password_btn = QPushButton("Change Password")
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.current_email)
        self.layout.addWidget(self.new_email)
        self.layout.addWidget(self.confirm_email)
        self.layout.addWidget(self.change_email_btn)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.current_password)
        self.layout.addWidget(self.new_password)
        self.layout.addWidget(self.confirm_password)
        self.layout.addWidget(self.change_password_btn)
        self.setLayout(self.layout)

