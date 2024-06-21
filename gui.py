import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QComboBox, QCalendarWidget, QDialog, QDialogButtonBox,
    QListWidget, QSpinBox
)
from PyQt6.QtCore import Qt

from flight_search import FlightSearch

class FlightSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Origin Input
        origin_layout = QHBoxLayout()
        origin_label = QLabel('Origin:')
        self.origin_input = QLineEdit()
        origin_layout.addWidget(origin_label)
        origin_layout.addWidget(self.origin_input)

        # Destination Input
        destination_layout = QVBoxLayout()
        destination_label = QLabel('Destinations:')
        self.destination_input = QLineEdit()
        self.add_destination_button = QPushButton('Add Destination')
        self.add_destination_button.clicked.connect(self.add_destination)
        self.destination_list = QListWidget()
        destination_layout.addWidget(destination_label)
        destination_layout.addWidget(self.destination_input)
        destination_layout.addWidget(self.add_destination_button)
        destination_layout.addWidget(self.destination_list)

        # Start Date Input
        start_date_layout = QHBoxLayout()
        start_date_label = QLabel('Start Date:')
        self.start_date_input = QPushButton('Select Date')
        self.start_date_input.clicked.connect(self.show_start_calendar)
        self.start_date_label = QLabel('Not Selected')
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(self.start_date_input)
        start_date_layout.addWidget(self.start_date_label)

        # End Date Input
        end_date_layout = QHBoxLayout()
        end_date_label = QLabel('End Date:')
        self.end_date_input = QPushButton('Select Date')
        self.end_date_input.clicked.connect(self.show_end_calendar)
        self.end_date_label = QLabel('Not Selected')
        end_date_layout.addWidget(end_date_label)
        end_date_layout.addWidget(self.end_date_input)
        end_date_layout.addWidget(self.end_date_label)

        # Duration of Stay Input
        duration_layout = QHBoxLayout()
        duration_label = QLabel('Duration of Stay (days):')
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(1)
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_input)

        # Class Selection
        class_layout = QHBoxLayout()
        class_label = QLabel('Class:')
        self.class_selection = QComboBox()
        self.class_selection.addItems(['Economy', 'Business', 'First'])
        class_layout.addWidget(class_label)
        class_layout.addWidget(self.class_selection)

        # Search Button
        self.search_button = QPushButton('Search Flights')
        self.search_button.clicked.connect(self.search_flights)

        # Add all layouts to the main layout
        main_layout.addLayout(origin_layout)
        main_layout.addLayout(destination_layout)
        main_layout.addLayout(start_date_layout)
        main_layout.addLayout(end_date_layout)
        main_layout.addLayout(duration_layout)
        main_layout.addLayout(class_layout)
        main_layout.addWidget(self.search_button)

        # Set main layout
        self.setLayout(main_layout)

        # Set window title and size
        self.setWindowTitle('Flight Search App')
        self.resize(400, 300)

    def add_destination(self):
        destination = self.destination_input.text()
        if destination:
            self.destination_list.addItem(destination)
            self.destination_input.clear()

    def show_start_calendar(self):
        self.calendar_dialog = CalendarDialog(self)
        if self.calendar_dialog.exec():
            self.start_date_label.setText(self.calendar_dialog.selected_date.toString('yyyy-MM-dd'))

    def show_end_calendar(self):
        self.calendar_dialog = CalendarDialog(self)
        if self.calendar_dialog.exec():
            self.end_date_label.setText(self.calendar_dialog.selected_date.toString('yyyy-MM-dd'))

    def search_flights(self):
        origin = self.origin_input.text()
        destinations = [self.destination_list.item(i).text() for i in range(self.destination_list.count())]
        start_date = self.start_date_label.text()
        end_date = self.end_date_label.text()
        duration_of_stay = self.duration_input.value()
        flight_class = self.class_selection.currentText()
        
        flight_data = {
            'origin': origin,
            'originLocationCode': None,
            'destinations': destinations,
            'destinationsLocationCodes': [],
            'departureDate' : start_date,
            'returnDate': end_date,
            'durationOfStay': duration_of_stay,
            'adults': 2,
            'currencyCode': 'PLN',
            'max': 50
        }

        fs = FlightSearch()
        fs.flight_search(flight_data)

        print(f"Searching for flights from {origin} to {', '.join(destinations)}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Duration of Stay: {duration_of_stay} days")
        print(f"Class: {flight_class}")
        # Here, you would typically call an API to search for flights and display the results
        return

class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Date')

        self.layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        self.layout.addWidget(self.calendar)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.selected_date = None

    def accept(self):
        self.selected_date = self.calendar.selectedDate()
        super().accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlightSearchApp()
    ex.show()
    sys.exit(app.exec())