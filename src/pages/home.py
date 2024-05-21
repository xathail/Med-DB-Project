from PyQt6.QtCore import QTimer, QDateTime, Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFormLayout, QLineEdit, QComboBox, QStackedLayout, QSpinBox, QDoubleSpinBox, QDateTimeEdit, QCheckBox, QMessageBox
import sqlite3
import os
import json

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # User form
        self.user_form = QFormLayout()
        self.user_type = QComboBox()
        self.user_type.addItems(["Child", "Admin"])
        self.user_name = QLineEdit()
        self.user_age = QSpinBox()
        self.user_form.addRow("Type:", self.user_type)
        self.user_form.addRow("Name:", self.user_name)
        self.user_form.addRow("Age:", self.user_age)
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)
        self.layout.addLayout(self.user_form)
        self.layout.addWidget(self.add_user_button)

        # Medication form
        self.med_form = QFormLayout()
        self.med_name = QLineEdit()
        self.med_min_interval = QSpinBox()
        self.med_max_dose = QSpinBox()
        self.med_age_appropriate = QLineEdit()
        self.med_form.addRow("Name:", self.med_name)
        self.med_form.addRow("Min Interval:", self.med_min_interval)
        self.med_form.addRow("Max Dose:", self.med_max_dose)
        self.med_form.addRow("Age Appropriate:", self.med_age_appropriate)
        self.add_med_button = QPushButton("Add Medication")
        self.add_med_button.clicked.connect(self.add_medication)
        self.layout.addLayout(self.med_form)
        self.layout.addWidget(self.add_med_button)

        # Reminder form
        self.reminder_form = QFormLayout()
        self.reminder_person_id = QSpinBox()
        self.reminder_med_id = QSpinBox()
        self.reminder_time = QDateTimeEdit()
        self.reminder_time.setDateTime(QDateTime.currentDateTime())
        self.reminder_active = QCheckBox()
        self.reminder_form.addRow("Person ID:", self.reminder_person_id)
        self.reminder_form.addRow("Medication ID:", self.reminder_med_id)
        self.reminder_form.addRow("Reminder Time:", self.reminder_time)
        self.reminder_form.addRow("Active:", self.reminder_active)
        self.add_reminder_button = QPushButton("Add Reminder")
        self.add_reminder_button.clicked.connect(self.add_reminder)
        self.layout.addLayout(self.reminder_form)
        self.layout.addWidget(self.add_reminder_button)

        # Refresh button
        self.refresh_button = QPushButton("Refresh Database")
        self.refresh_button.clicked.connect(self.refresh_database)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        # Timer to update reminder_time every minute
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_reminder_time)
        self.timer.start(60000)  # 60000 milliseconds = 1 minute

        # Get database location from config.json
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')) as f:
            self.db_location = json.load(f)['databaseLocation']

    def add_user(self):
        conn = sqlite3.connect(self.db_location)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO people (name, age, type)
            VALUES (?, ?, ?)
        """, (self.user_name.text(), self.user_age.value(), self.user_type.currentText()))
        conn.commit()
        conn.close()

        # Confirmation message
        QMessageBox.information(self, "User Added", f"[{self.user_type.currentText()}] {self.user_name.text()} has been added to the database.")


    def add_medication(self):
        conn = sqlite3.connect(self.db_location)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medications (name, min_interval, max_dose_per_day, age_appropriate)
            VALUES (?, ?, ?, ?)
        """, (self.med_name.text(), self.med_min_interval.value(), self.med_max_dose.value(), self.med_age_appropriate.text()))
        conn.commit()
        conn.close()

        # Confirmation message
        QMessageBox.information(self, "Medication Added", f"{self.med_name.text()} has been added to the database.")

    def add_log(self):
        conn = sqlite3.connect(self.db_location)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO log (person_id, medication_id, added_time)
            VALUES (?, ?, ?)
        """, (self.log_person_id.value(), self.log_med_id.value(), self.log_added_time.dateTime().toString(Qt.ISODate)))
        conn.commit()
        conn.close()

    def add_reminder(self):
        conn = sqlite3.connect(self.db_location)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reminders (person_id, medication_id, reminder_time, active)
            VALUES (?, ?, ?, ?)
        """, (self.reminder_person_id.value(), self.reminder_med_id.value(), self.reminder_time.dateTime().toString(Qt.ISODate), self.reminder_active.isChecked()))
        reminder_id = cursor.lastrowid  # Get the ID of the newly inserted reminder

        # Log the creation of the reminder
        cursor.execute("""
            INSERT INTO log (reminder_id, action, timestamp)
            VALUES (?, ?, ?)
        """, (reminder_id, "Reminder created", QDateTime.currentDateTime().toString(Qt.ISODate)))

        conn.commit()
        conn.close()

        # Confirmation message
        QMessageBox.information(self, "Reminder Added", f"Reminder for person {self.reminder_person_id.value()} for medication {self.reminder_med_id.value()} has been added to the database.")

    def update_reminder_time(self):
        self.reminder_time.setDateTime(QDateTime.currentDateTime())

    def refresh_database(self):
        try:
            conn = sqlite3.connect(self.db_location)
            conn.close()

            # Confirmation message
            QMessageBox.information(self, "Refresh Database", "Database has been refreshed.")
        except sqlite3.OperationalError:
            # Error message
            QMessageBox.critical(self, "Refresh Database", "Failed to refresh the database. Please check the database file.")