import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QMessageBox, QComboBox, QFileDialog, QScrollArea, QDateEdit, QDialog,
                             QGridLayout, QInputDialog, QCalendarWidget)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QDate, Qt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date as dt, timedelta
from typing import List

class Expense:
    def __init__(self, description: str, amount: float, category: str, date: dt = None):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date if date else dt.today()
    
    def __repr__(self) -> str:
        return f"{self.date.strftime('%Y-%m-%d')} - {self.description}: £{self.amount:.2f} ({self.category})"
    
    def to_dict(self) -> dict:
        return {'description': self.description, 'amount': self.amount, 'category': self.category, 'date': self.date.isoformat()}
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['description'], data['amount'], data['category'], dt.fromisoformat(data['date']) if 'date' in data else None)

class ExpenseTracker:
    def __init__(self, username):
        self.username = username
        self.expenses_directory = os.path.join(os.path.dirname(__file__), 'data', 'expenses')
        os.makedirs(self.expenses_directory, exist_ok=True)
        self.expenses_file = os.path.join(self.expenses_directory, f'{username}_expenses.json')
        self.expenses: List[Expense] = []
        self.load_from_file(self.expenses_file)

    def add_expense(self, description: str, amount: float, category: str, date: dt) -> None:
        expense = Expense(description, amount, category, date)
        self.expenses.append(expense)

    def edit_expense(self, index: int, description: str, amount: float, category: str, date: dt) -> None:
        if 0 <= index < len(self.expenses):
            self.expenses[index] = Expense(description, amount, category, date)

    def delete_expense(self, index: int) -> None:
        if 0 <= index < len(self.expenses):
            del self.expenses[index]

    def total_expenses(self) -> float:
        return sum(expense.amount for expense in self.expenses)

    def save_to_file(self) -> None:
        try:
            with open(self.expenses_file, 'w') as file:
                json.dump([expense.to_dict() for expense in self.expenses], file, indent=4)
        except IOError as e:
            QMessageBox.critical(None, "File Error", f"Failed to save expenses: {e}")

    def load_from_file(self, filename: str) -> None:
        try:
            with open(filename, 'r') as file:
                expenses_data = json.load(file)
                self.expenses = [Expense.from_dict(data) for data in expenses_data]
        except FileNotFoundError:
            QMessageBox.warning(None, "File Not Found", "No previous expense file found, starting fresh.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(None, "File Error", f"Failed to parse '{filename}': {e}")

    def get_expenses_in_range(self, start_date: dt, end_date: dt) -> List[Expense]:
        return [expense for expense in self.expenses if start_date <= expense.date <= end_date]

    def generate_report(self, report_type: str) -> dict:
        today = dt.today()
        if report_type == 'weekly':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif report_type == 'monthly':
            start_date = today.replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        elif report_type == 'yearly':
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        else:
            raise ValueError("Invalid report type")

        expenses = self.get_expenses_in_range(start_date, end_date)
        total = sum(expense.amount for expense in expenses)
        by_category = {}
        for expense in expenses:
            by_category[expense.category] = by_category.get(expense.category, 0) + expense.amount

        return {
            'start_date': start_date,
            'end_date': end_date,
            'total': total,
            'by_category': by_category
        }

    def plot_expense_distribution(self):
        categories = [expense.category for expense in self.expenses]
        category_counts = {category: categories.count(category) for category in set(categories)}

        plt.figure(figsize=(8,6))
        plt.pie(category_counts.values(), labels=category_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution by Category')
        plt.axis('equal')
        plt.show()

class UserManager:
    def __init__(self):
        self.users_directory = os.path.join(os.path.dirname(__file__), 'data', 'users')
        os.makedirs(self.users_directory, exist_ok=True)
        self.users_file = os.path.join(self.users_directory, 'users.json')
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                return json.load(file)
        return {'admin': 'password123'}
    
    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, username: str, password: str):
        self.users[username] = password
        self.save_users() 

    def authenticate(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class LoginDialog(QDialog):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.authenticated = False
        self.authenticated_username = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 120)

        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.user_manager.authenticate(username, password):
            self.authenticated = True
            self.authenticated_username = username
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Please try again.")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            if username in self.user_manager.users:
                QMessageBox.warning(self, 'Registration Failed', 'Username already exists. Please choose another.')
            else:
                self.user_manager.add_user(username, password)
                QMessageBox.information(self, 'Registration Successful', 'You can now log in with your new account.')
        else:
            QMessageBox.warning(self, 'Registration Failed', 'Please enter both username and password.')

class ExpenseTrackerApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.tracker = ExpenseTracker(username)
        
        self.setWindowTitle(f"Expense Tracker - {username}")
        self.setGeometry(200, 200, 600, 400)

        self.dark_mode = False

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields
        input_layout = QGridLayout()
        self.desc_label = QLabel("Description:")
        self.desc_input = QLineEdit()
        self.amount_label = QLabel("Amount (£):")
        self.amount_input = QLineEdit()
        self.amount_input.setValidator(QDoubleValidator(0.0, 10000.0, 2))
        self.category_label = QLabel("Category:")
        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Transport", "Entertainment", "Housing", "Utilities", "Healthcare", "Education", "Shopping", "Other"])
        self.date_label = QLabel('Date:')
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        input_layout.addWidget(self.desc_label, 0, 0)
        input_layout.addWidget(self.desc_input, 0, 1)
        input_layout.addWidget(self.amount_label, 0, 2)
        input_layout.addWidget(self.amount_input, 0, 3)
        input_layout.addWidget(self.category_label, 1, 0)
        input_layout.addWidget(self.category_input, 1, 1)
        input_layout.addWidget(self.date_label, 1, 2)
        input_layout.addWidget(self.date_input, 1, 3)

        layout.addLayout(input_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Expense")
        self.add_btn.clicked.connect(self.add_expense)
        self.edit_btn = QPushButton("Edit Expense")
        self.edit_btn.clicked.connect(self.edit_expense)
        self.delete_btn = QPushButton("Delete Expense")
        self.delete_btn.clicked.connect(self.delete_expense)
        self.total_btn = QPushButton("Show Total")
        self.total_btn.clicked.connect(self.show_total)
        self.save_btn = QPushButton("Save Expenses")
        self.save_btn.clicked.connect(self.save_expenses)
        self.export_btn = QPushButton("Export to Excel")
        self.export_btn.clicked.connect(self.export_to_excel)
        self.visualize_btn = QPushButton("Visualize Expenses")
        self.visualize_btn.clicked.connect(self.tracker.plot_expense_distribution)
        self.theme_btn = QPushButton("Toggle Dark Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.total_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.visualize_btn)
        btn_layout.addWidget(self.theme_btn)

        layout.addLayout(btn_layout)

        # Expense list
        self.expense_list = QListWidget()
        self.load_expenses()

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.expense_list)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)

        # Report buttons
        report_layout = QHBoxLayout()
        self.weekly_report_btn = QPushButton("Weekly Report")
        self.weekly_report_btn.clicked.connect(lambda: self.show_report('weekly'))
        self.monthly_report_btn = QPushButton("Monthly Report")
        self.monthly_report_btn.clicked.connect(lambda: self.show_report('monthly'))
        self.yearly_report_btn = QPushButton("Yearly Report")
        self.yearly_report_btn.clicked.connect(lambda: self.show_report('yearly'))

        report_layout.addWidget(self.weekly_report_btn)
        report_layout.addWidget(self.monthly_report_btn)
        report_layout.addWidget(self.yearly_report_btn)

        layout.addLayout(report_layout)

        self.setLayout(layout)

    def add_expense(self):
        description = self.desc_input.text()
        amount = float(self.amount_input.text()) if self.amount_input.text() else 0
        category = self.category_input.currentText()
        date = self.date_input.date().toPyDate()

        if not description or amount <= 0:
            QMessageBox.warning(self, "Input Error", "Please enter a valid description and amount.")
            return

        self.tracker.add_expense(description, amount, category, date)
        self.expense_list.addItem(str(self.tracker.expenses[-1]))
        self.clear_inputs()

    def edit_expense(self):
        current_item = self.expense_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to edit.")
            return

        index = self.expense_list.currentRow()
        expense = self.tracker.expenses[index]

        self.desc_input.setText(expense.description)
        self.amount_input.setText(str(expense.amount))
        self.category_input.setCurrentText(expense.category)
        self.date_input.setDate(QDate.fromString(expense.date.isoformat(), Qt.ISODate))

        if self.get_expense_details():
            description = self.desc_input.text()
            amount = float(self.amount_input.text())
            category = self.category_input.currentText()
            date = self.date_input.date().toPyDate()

            self.tracker.edit_expense(index, description, amount, category, date)
            self.expense_list.takeItem(index)
            self.expense_list.insertItem(index, str(self.tracker.expenses[index]))
            self.clear_inputs()

    def delete_expense(self):
        current_item = self.expense_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Selection Error", "Please select an expense to delete.")
            return

        index = self.expense_list.currentRow()
        reply = QMessageBox.question(self, 'Delete Expense', 'Are you sure you want to delete this expense?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.tracker.delete_expense(index)
            self.expense_list.takeItem(index)

    def clear_inputs(self):
        self.desc_input.clear()
        self.amount_input.clear()
        self.category_input.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())

    def load_expenses(self):
        self.expense_list.clear()
        for expense in self.tracker.expenses:
            self.expense_list.addItem(str(expense))

    def export_to_excel(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save as Excel File", "", "Excel Files (*.xlsx)")
            if filename:
                df = pd.DataFrame([expense.to_dict() for expense in self.tracker.expenses])
                df.to_excel(filename, index=False)
                QMessageBox.information(self, "Success", f"Expenses exported successfully to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export expenses: {e}")

    def show_total(self):
        total = self.tracker.total_expenses()
        QMessageBox.information(self, "Total Expenses", f"Total expenses: £{total:.2f}")

    def save_expenses(self):
        self.tracker.save_to_file()
        QMessageBox.information(self, "Save", "Expenses saved successfully.")

    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")
            self.dark_mode = False
        else:
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.dark_mode = True

    def show_report(self, report_type):
        report = self.tracker.generate_report(report_type)
        
        message = f"{report_type.capitalize()} Report\n"
        message += f"From {report['start_date']} to {report['end_date']}\n\n"
        message += f"Total Expenses: £{report['total']:.2f}\n\n"
        message += "Expenses by Category:\n"
        for category, amount in report['by_category'].items():
            message += f"{category}: £{amount:.2f}\n"

        QMessageBox.information(self, f"{report_type.capitalize()} Report", message)

    def get_expense_details(self):
        return QMessageBox.Yes == QMessageBox.question(self, 'Confirm Edit', 'Are you sure you want to edit this expense?',
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def closeEvent(self, event):
        self.save_expenses()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    user_manager = UserManager()
    login_dialog = LoginDialog(user_manager)

    if login_dialog.exec() == QDialog.Accepted and login_dialog.authenticated:
        main_window = ExpenseTrackerApp(login_dialog.authenticated_username)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()