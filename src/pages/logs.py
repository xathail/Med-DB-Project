from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QFrame, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtCore import Qt
import os
import json
import sqlite3
import pandas as pd

class LogsPage(QWidget):
    def __init__(self):
        super().__init__()
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')) as f:
            self.db_location = json.load(f)['databaseLocation']
        self.layout = QVBoxLayout()

        # Recent reminders section
        self.reminders_label = QLabel("Recent reminders")
        self.reminders_label.setFont(QFont('Arial', 12))
        self.reminders_box = QTextEdit()
        self.reminders_box.setReadOnly(True)
        self.reminders_box.setFrameShape(QFrame.Shape.StyledPanel)
        self.reminders_box.setFrameShadow(QFrame.Shadow.Sunken)
        self.reminders_box.setLineWidth(2)
        self.reminders_box.setMidLineWidth(3)
        self.reminders_box.setContentsMargins(6, 6, 6, 6)  # Set the margins to create the rounded corners
        # Load logs from the database
        self.load_logs()

        # Export buttons for reminders
        self.reminders_export_layout = QHBoxLayout()
        self.reminders_export_csv = QPushButton("Export as .csv")
        self.reminders_export_json = QPushButton("Export as .json")
        self.reminders_export_xlsx = QPushButton("Export as .xlsx")
        self.reminders_export_layout.addWidget(self.reminders_export_csv)
        self.reminders_export_layout.addWidget(self.reminders_export_json)
        self.reminders_export_layout.addWidget(self.reminders_export_xlsx)

        # Connect export buttons to their respective methods
        self.reminders_export_csv.clicked.connect(lambda: self.export_data('reminders', 'csv'))
        self.reminders_export_json.clicked.connect(lambda: self.export_data('reminders', 'json'))
        self.reminders_export_xlsx.clicked.connect(lambda: self.export_data('reminders', 'xlsx'))



        # Admin logs section
        """
        self.admin_logs_label = QLabel("Admin logs")
        self.admin_logs_label.setFont(QFont('Arial', 12))
        self.admin_logs_box = QTextEdit()
        self.admin_logs_box.setReadOnly(True)
        self.admin_logs_box.setFrameShape(QFrame.Shape.StyledPanel)
        self.admin_logs_box.setFrameShadow(QFrame.Shadow.Sunken)
        self.admin_logs_box.setLineWidth(2)
        self.admin_logs_box.setMidLineWidth(3)
        self.admin_logs_box.setContentsMargins(6, 6, 6, 6)  # Set the margins to create the rounded corners

        # Export buttons for admin logs
        self.admin_logs_export_layout = QHBoxLayout()
        self.admin_logs_export_csv = QPushButton("Export as .csv")
        self.admin_logs_export_json = QPushButton("Export as .json")
        self.admin_logs_export_xlsx = QPushButton("Export as .xlsx")
        self.admin_logs_export_layout.addWidget(self.admin_logs_export_csv)
        self.admin_logs_export_layout.addWidget(self.admin_logs_export_json)
        self.admin_logs_export_layout.addWidget(self.admin_logs_export_xlsx)

        # Connect export buttons to their respective methods
        self.admin_logs_export_csv.clicked.connect(lambda: self.export_data('admin_logs', 'csv'))
        self.admin_logs_export_json.clicked.connect(lambda: self.export_data('admin_logs', 'json'))
        self.admin_logs_export_xlsx.clicked.connect(lambda: self.export_data('admin_logs', 'xlsx'))
        """

        # Add widgets to the main layout
        self.layout.addWidget(self.reminders_label)
        self.layout.addWidget(self.reminders_box)
        self.layout.addLayout(self.reminders_export_layout)
        """
        self.layout.addWidget(self.admin_logs_label)
        self.layout.addWidget(self.admin_logs_box)
        self.layout.addLayout(self.admin_logs_export_layout)
        """
        self.setLayout(self.layout)

    def load_logs(self):
        conn = sqlite3.connect(self.db_location)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.id, p.name, m.name, l.action, l.timestamp
            FROM log l
            JOIN reminders r ON l.reminder_id = r.id
            JOIN people p ON r.person_id = p.id
            JOIN medications m ON r.medication_id = m.id
        """)
        logs = cursor.fetchall()

        for log_id, person, medication, action, timestamp in logs:
            self.reminders_box.append(f"ID: {log_id}, Person: {person}, Medication: {medication}, Action: {action}, Timestamp: {timestamp}")

        conn.close()

    def export_data(self, table_name, file_format):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r') as f:
            data = json.load(f)
            db_path = data['databaseLocation']
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                if file_format == 'csv':
                    df.to_csv(f"{table_name}.csv", index=False)
                elif file_format == 'json':
                    df.to_json(f"{table_name}.json", orient='records')
                elif file_format == 'xlsx':
                    df.to_excel(f"{table_name}.xlsx", index=False)
                conn.close()
                QMessageBox.information(self, "Success", f"{table_name} successfully exported as {file_format}.")
            else:
                QMessageBox.warning(self, "Failed", "Database does not exist.")