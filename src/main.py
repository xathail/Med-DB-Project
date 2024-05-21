from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QFrame, QHBoxLayout
from PyQt6 import QtCore
from qtawesome import icon
from PyQt6.QtWidgets import QButtonGroup, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon, QAction

from pages.user_settings import UserSettingsPage
from pages.logs import LogsPage
from pages.managedb import ManagedbPage
from pages.reminders import RemindersPage
from pages.home import HomePage

class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setFixedWidth(150)
        self.setStyleSheet("background-color: lightgrey;")  # Set the color of the sidebar
        self.buttons = {
            "hamburger": QPushButton(icon('fa5s.bars'), ""),  # Add the hamburger button here
            "home": QPushButton(icon('fa5s.home'), "Home"),
            "reminders": QPushButton(icon('fa5s.bell'), "Reminders"),
            "managedb": QPushButton(icon('fa5s.database'), "Manage DB"),
            "logs": QPushButton(icon('fa5s.book'), "Logs"),
            "settings": QPushButton(icon('fa5s.cog'), "User Settings"),
        }
        self.buttons["hamburger"].setFixedWidth(22)  # Set the width of the hamburger button
        self.button_group = QButtonGroup()  # Create a button group
        for btn in self.buttons.values():
            btn.setCheckable(True)
            btn.setIconSize(QtCore.QSize(22, 22))
            btn.setStyleSheet('''
                QPushButton {
                    text-align: left;
                    background-color: lightgrey;
                }
                QPushButton:checked {
                    background-color: lightblue;
                }
            ''')  # Set the style of the button
            self.layout.addWidget(btn)
            self.button_group.addButton(btn)
        self.setLayout(self.layout)
        self.buttons["home"].setChecked(True)  # Set the "Home" button as checked

class MainWindow(QMainWindow):
    def __init__(self, width=725, height=300):
        super().__init__()
        self.setWindowTitle("MedTool+")
        self.setWindowIcon(QIcon("assets/img/logo.png"))  # Set the application icon
        self.resize(width, height)  # Set the initial size of the window
        self.main_widget = QStackedWidget()
        self.sidebar = SideBar()
        self.home_page = HomePage()  # Create the home page
        self.reminders_page = RemindersPage()  # Create the reminders page
        self.managedb_page = ManagedbPage()  # Create the manage database page
        self.logs_page = LogsPage()  # Create the logs page
        self.user_settings_page = UserSettingsPage()  # Create the user settings page
        self.main_widget.addWidget(self.home_page)
        self.main_widget.addWidget(self.reminders_page)
        self.main_widget.addWidget(self.managedb_page)
        self.main_widget.addWidget(self.logs_page)
        self.main_widget.addWidget(self.user_settings_page)
        self.sidebar.buttons["settings"].clicked.connect(lambda: self.main_widget.setCurrentIndex(self.main_widget.count() - 1))
        self.sidebar.buttons["hamburger"].clicked.connect(self.toggle_sidebar)  # Connect the hamburger button to the toggle_sidebar method
        self.central_widget = QWidget()  # Create a central widget
        self.layout = QHBoxLayout(self.central_widget)  # Set the layout of the central widget
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.main_widget)
        self.setCentralWidget(self.central_widget)  # Set the central widget of the main window
        self.connect_signals()
        self.main_widget.setCurrentIndex(0)  # Set the current index to 0

    def toggle_sidebar(self):
        for btn in self.sidebar.buttons.values():
            if btn.text() != "":  # Exclude the hamburger button
                btn.setVisible(not btn.isVisible())  # Toggle the visibility of the button

    def connect_signals(self):
        self.sidebar.buttons["home"].clicked.connect(lambda: self.main_widget.setCurrentIndex(0))
        self.sidebar.buttons["reminders"].clicked.connect(lambda: self.main_widget.setCurrentIndex(1))
        self.sidebar.buttons["managedb"].clicked.connect(lambda: self.main_widget.setCurrentIndex(2))
        self.sidebar.buttons["logs"].clicked.connect(lambda: self.main_widget.setCurrentIndex(3))
        self.sidebar.buttons["settings"].clicked.connect(lambda: self.main_widget.setCurrentIndex(4))
    

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()