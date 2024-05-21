from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QTimer, QDateTime, Qt
import sqlite3
import os
import json

class RemindersPage(QWidget):
    def __init__(self):
        super().__init__()
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')) as f:
            self.db_location = json.load(f)['databaseLocation']
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # Update every second

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect(self.db_location)
        cursor = conn.cursor()

        # Check if the reminders table exists
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='reminders';
        """)
        if cursor.fetchone() is None:
            # The reminders table does not exist, so return without loading data
            conn.close()
            return

        cursor.execute("""
            SELECT r.id, p.name, m.name, r.reminder_time, r.active
            FROM reminders r
            JOIN people p ON r.person_id = p.id
            JOIN medications m ON r.medication_id = m.id
            WHERE r.active = 1
        """)
        reminders = cursor.fetchall()

        self.table.setRowCount(len(reminders))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Person", "Medication", "Reminder Time", "Countdown"])

        for i, (id, person, medication, reminder_time, active) in enumerate(reminders):
            self.table.setItem(i, 0, QTableWidgetItem(str(id)))
            self.table.setItem(i, 1, QTableWidgetItem(person))
            self.table.setItem(i, 2, QTableWidgetItem(medication))
            self.table.setItem(i, 3, QTableWidgetItem(reminder_time))
            self.table.setItem(i, 4, QTableWidgetItem(""))  # Countdown will be updated by update_countdown

        conn.close()

    def update_countdown(self):
        current_time = QDateTime.currentDateTime()

        for i in range(self.table.rowCount()):
            reminder_time = QDateTime.fromString(self.table.item(i, 3).text(), Qt.ISODate)

            if reminder_time > current_time:
                countdown = current_time.secsTo(reminder_time)
                hours, remainder = divmod(countdown, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.table.setItem(i, 4, QTableWidgetItem(f"{hours:02}:{minutes:02}:{seconds:02}"))
            else:
                self.table.setItem(i, 4, QTableWidgetItem("Time's up!"))