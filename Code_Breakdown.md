# Expense-Tracker

Code breakdown and its function purspose.

Welcome to where I explain my code and what it does.

Below is a short explaination of what the libraries I have imported does.

Library Imports:

import sys
import json
import os
from datetime import date as dt, timedelta
from typing import List

sys - I use this to interect with the Python runtime environment and with PyQT it handles system-level functions, such as to close the program (sys.exit())

json - This is the main functions I use to parse and manipulate JSON date - bascliy I use this to save, load and process my data.

os - This provides the functions I use to interact with the operating system so that I can create the data directories for saving user profiles and checking if a file path exists.

datetime - I use dt to represent the current date and time when logging expenses - giving them a time stamp for calculating the range of dates(useful with timedelta) or visualization - my Pie chart.

from typing import list - Is used to make my code more readable and maintainable, so I can read it better when finding the errors.

PyQt5 Modules -

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QComboBox, QFileDialog, QScrollArea, QDateEdit, QDialog, QGridLayout, QInputDialog, QCalendarWidget, QDialogButtonBox)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QDate, Qt

Okay this next part is a lot so I may be just giving general googled anwsers to help speed things along.

QApplication - Manages application-wide settings and main event loop, it is required to start any PyQt application.

QWidget - The base class for all UI objests - It baslicly serves as a container for other widgets.

Layouts - Used to organize and position the widgets in the application.

    QVBoxLayout - Vertical layout, Stacks child widgets vertically.
    QHBoxLayout - Horizontal layout, Stacks child widgets horizontally.
    QGridLayout - Arranges widgets in a grid with rows and columns, giving more flexibility.

Widgets - Building blocks of the GUI.

    QLabel: Displays text or images.
    QLineEdit: Provides a text input field.
    QPushButton: Creates a clickable button.
    QListWidget: Displays a list of items, such as expense categories.
    QComboBox: Creates a drop-down menu for selecting options.
    QDateEdit: Allows users to select a date.
    QCalendarWidget: Provides a calendar view for date selection.
    QDialog and QDialogButtonBox: Used for pop-up dialog windows with buttons (e.g., Ok, Cancel).

File handling:

    QFileDialog - Opens file dialog boxes to let users select a file to open or save data.

Validation and Formatting:

    QDoubleValidator - Ensures that text input is a valid floating-point number. Useful for fields where users need to enter amounts for expenses.

Core Modules.

    QDate - Reprensents a date in the PyQt context.

    Qt - Provides constaints for various purposes, such as alignment or key codes.

Data Analysis and Visualization:

The two libraries are widely used for data analysis and visualization.

import pandas as pd
import matplotlib.pyplot as plt

pandas - Data manipulation library, used for working with structured data like expense records. Can be used to store, filter, and analyse data in a tabular format.

matplotlib.pyplot - A plotting library used to create graphs and charts.

Class Expense - what it does and why.

The below is a breakdown of the Class Expense, why it is there and what the function of this class does in the app.

class Expense:
    def __init__(self, description: str, amount: float, category: str, date: dt = None):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date if date else dt.today()

The class Expense serves as a blueprint for creating expense objects. Each expense will have certain attributes, making it easy to store and manipulate data consistenly.

The below ensures that every expense has a description, amount, category and date.

__init__: This is the class constructor, it is called when a new expense object is created. It initializes the following:

    description(str) - A breif description of what the expense is for, such as "KFC" or "Clothes".

    amount(float) - The cost of the expense in a numeric form,which can be used for calculations and analysis.(Total expenses etc)

    category(str) - The category or type of the expense, such as "Food" or "Rent". Helps to group and filter expenses for pie chart etc.

    date(datetime.date) the date when the expense inclurred. will default to current date if no date is entered, which is important for reports and filtering analysis.

def __repr__(self) -> str:
    return f"{self.date.strftime('%Y-%m-%d')} - {self.description}: £{self.amount:.2f} ({self.category})"

The __repr__ provides a String representation of the expense data, making it readable when printed or viewed in lists.
It formats the data so that the output will look a bit like this: "2024-10-07 - KFC £12.00 (Food)"

def to_dict(self) -> dict:
    return {'description': self.description, 'amount': self.amount, 'category': self.category, 'date': self.date.isoformat()}

This changes the expanse data into a dictionary format (dict) for easy storage and manipulation. It is used typically when you want to save data to a file (e.g. JSON formay) or transfer it between parts of the application. The description, amount and category are stored directly as their values, while date is converted into ISO format (YYYY-MM-DD) using the isoformat() method. This ensures data is stored consistently and can be parsed back later easily.

@classmethod
def from_dict(cls, data: dict):
    return cls(data['description'], data['amount'], data['category'], dt.fromisoformat(data['date']) if 'date' in data else None)

This class method is used to take information from an dictionary as arguments and returns it as a Expense object. Used to return data from saved files and recreate them in the app. It extracts the values as normal for description, amount and category and coverts the date from ISO format back into a datetime.date object using the dt.fromisoformat().

