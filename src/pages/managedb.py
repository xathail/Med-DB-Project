import os
import json
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from shutil import copyfile

import sqlite3

class ManagedbPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Create DB button
        self.create_db_button = QPushButton("Create DB")
        self.create_db_button.clicked.connect(self.create_db)
        self.layout.addWidget(self.create_db_button)

        # Delete DB button
        self.delete_db_button = QPushButton("Delete DB")
        self.delete_db_button.clicked.connect(self.delete_db)
        self.layout.addWidget(self.delete_db_button)

        # Create backup button
        self.create_backup_button = QPushButton("Create Backup")
        self.create_backup_button.clicked.connect(self.create_backup)
        self.layout.addWidget(self.create_backup_button)

        # Rename DB section
        self.rename_db_layout = QHBoxLayout()
        self.rename_db_input = QLineEdit()
        self.rename_db_button = QPushButton("Rename DB")
        self.rename_db_button.clicked.connect(self.rename_db)
        self.rename_db_layout.addWidget(self.rename_db_input)
        self.rename_db_layout.addWidget(self.rename_db_button)
        self.layout.addLayout(self.rename_db_layout)

        # Other useful buttons
        # Add other buttons as needed

        self.setLayout(self.layout)

    def create_db(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r+') as f:
            data = json.load(f)
            db_path = data['databaseLocation']
            if not db_path:  # If the JSON location is empty
                db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'new_database.db')
                data['databaseLocation'] = db_path
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Check if any tables exist in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            if not tables:  # If no tables exist, the database is considered empty
                # Create people table
                cursor.execute("""
                    CREATE TABLE people (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        type TEXT
                    )
                """)

                # Create medications table
                cursor.execute("""
                    CREATE TABLE medications (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        min_interval INTEGER,
                        max_dose_per_day INTEGER,
                        age_appropriate TEXT,
                        quantity INTEGER,
                        price REAL
                    )
                """)

                # Create log table
                cursor.execute("""
                    CREATE TABLE log (
                        id INTEGER PRIMARY KEY,
                        reminder_id INTEGER,
                        action TEXT,
                        timestamp TEXT
                    )
                """)

                # Create reminders table
                cursor.execute("""
                    CREATE TABLE reminders (
                        id INTEGER PRIMARY KEY,
                        person_id INTEGER,
                        medication_id INTEGER,
                        reminder_time TEXT,
                        active INTEGER,
                        FOREIGN KEY(person_id) REFERENCES people(id),
                        FOREIGN KEY(medication_id) REFERENCES medications(id)
                    )
                """)

                QMessageBox.information(self, "Success", "Database successfully created.")
                print(f"Database successfully created at {db_path}.")
            else:
                QMessageBox.warning(self, "Failed", "Database already exists and is not empty.")

            conn.close()
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def delete_db(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r+') as f:
            data = json.load(f)
            if os.path.exists(data['databaseLocation']):
                db_name = os.path.basename(data['databaseLocation'])
                confirm_name, ok = QInputDialog.getText(self, "Confirm Delete", f"Please re-enter the name of this db {db_name} in the textbox below:")
                if ok and confirm_name == db_name:
                    os.remove(data['databaseLocation'])
                    data['databaseLocation'] = ""
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    QMessageBox.information(self, "Success", "Database successfully deleted.")
                elif ok:
                    QMessageBox.warning(self, "Failed", "Database name does not match.")

    def create_backup(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r') as f:
            data = json.load(f)
            if os.path.exists(data['databaseLocation']):
                backup_path = data['databaseLocation'].replace('.db', '-backup.db')
                copyfile(data['databaseLocation'], backup_path)
                QMessageBox.information(self, "Success", "Backup successfully created.")

    def rename_db(self):
        new_name = self.rename_db_input.text()
        if not new_name.endswith('.db'):
            new_name += '.db'
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r+') as f:
            data = json.load(f)
            if os.path.exists(data['databaseLocation']):
                old_name = os.path.basename(data['databaseLocation'])
                new_path = os.path.join(os.path.dirname(data['databaseLocation']), new_name)
                os.rename(data['databaseLocation'], new_path)
                data['databaseLocation'] = new_path
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                QMessageBox.information(self, "Success", f"Successfully renamed {old_name} to {new_name}.")

