from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCalendarWidget, QListWidget, QSpinBox, QDialog, QDialogButtonBox
)

from FlightSearch import FlightSearch
from FareResultsDialog import ResultsDialog
from DestinationsResultDialog import DestinationsResultDialog


class FlightSearchApp(QWidget):
    """
    Class resposible for displaying main window GUI for flight search
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Function responsible for initializing GUI for main window
        """
        main_layout = QVBoxLayout()

        # Origin Input
        origin_layout = QHBoxLayout()
        origin_label = QLabel('Origin:')
        self.origin_input = QLineEdit()
        self.origin_input.setPlaceholderText('Krakow')
        self.destination_search_button = QPushButton('Search Destinations')
        self.destination_search_button.clicked.connect(self.search_destinations)
        origin_layout.addWidget(origin_label)
        origin_layout.addWidget(self.origin_input)
        origin_layout.addWidget(self.destination_search_button)

        # Destination Input
        destination_layout_H = QHBoxLayout()
        destination_layout_V = QVBoxLayout()
        destination_label = QLabel('Destinations:')
        self.destination_input = QLineEdit()
        self.add_destination_button = QPushButton('Add Destination')
        self.add_destination_button.clicked.connect(self.add_destination)
        self.clear_destination_button = QPushButton('Clear Destinations')
        self.clear_destination_button.clicked.connect(self.clear_destinations)
        self.destination_list = QListWidget()
        destination_layout_H.addWidget(destination_label)
        destination_layout_H.addWidget(self.destination_input)
        destination_layout_H.addWidget(self.clear_destination_button)
        destination_layout_V.addLayout(destination_layout_H)
        destination_layout_V.addWidget(self.add_destination_button)
        destination_layout_V.addWidget(self.destination_list)

        # Start Date Input
        start_date_layout = QHBoxLayout()
        start_date_label = QLabel('Start Date:')
        self.start_date_input = QPushButton('Select Date')
        self.start_date_input.clicked.connect(self.show_start_calendar)
        self.start_date_label = QLabel('Not Selected')
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(self.start_date_label)
        start_date_layout.addWidget(self.start_date_input)

        # End Date Input
        end_date_layout = QHBoxLayout()
        end_date_label = QLabel('End Date:')
        self.end_date_input = QPushButton('Select Date')
        self.end_date_input.clicked.connect(self.show_end_calendar)
        self.end_date_label = QLabel('Not Selected')
        end_date_layout.addWidget(end_date_label)
        end_date_layout.addWidget(self.end_date_label)
        end_date_layout.addWidget(self.end_date_input)

        # Duration of Stay Input
        duration_layout = QHBoxLayout()
        duration_label = QLabel('Duration of stay (days):')
        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(1)
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_input)

        # Search Button
        self.search_button = QPushButton('Search Flights')
        self.search_button.clicked.connect(self.search_flights)

        # Add all layouts to the main layout
        main_layout.addLayout(origin_layout)
        main_layout.addLayout(destination_layout_V)
        main_layout.addLayout(start_date_layout)
        main_layout.addLayout(end_date_layout)
        main_layout.addLayout(duration_layout)
        main_layout.addWidget(self.search_button)

        # Set main layout
        self.setLayout(main_layout)

        # Set window title and size
        self.setWindowTitle('Flight Search App')
        self.resize(500, 600)

    def search_destinations(self):
        fs = FlightSearch()
        origin = self.origin_input.text()
        fs.destination_search(origin)

        self.results_dialog = DestinationsResultDialog(fs.desinations, origin)
        self.results_dialog.exec()

    def add_destination(self):
        destination = self.destination_input.text()
        if destination:
            self.destination_list.addItem(destination)
            self.destination_input.clear()

    def clear_destinations(self):
        self.destination_input.clear()
        self.destination_list.clear()

    def show_start_calendar(self):
        self.calendar_dialog = CalendarDialog(self)
        if self.calendar_dialog.exec():
            self.start_date_label.setText(
                self.calendar_dialog.selected_date.toString('yyyy-MM-dd'))

    def show_end_calendar(self):
        self.calendar_dialog = CalendarDialog(self)
        if self.calendar_dialog.exec():
            self.end_date_label.setText(
                self.calendar_dialog.selected_date.toString('yyyy-MM-dd'))

    def search_flights(self):
        origin = self.origin_input.text()
        destinations = [self.destination_list.item(
            i).text() for i in range(self.destination_list.count())]
        start_date = self.start_date_label.text()
        end_date = self.end_date_label.text()
        minimal_duration = self.duration_input.value()

        flight_data = {
            'origin': origin,
            'originLocationCode': [],
            'destination': destinations,
            'destinationLocationCode': [],
            'departureDate': start_date,
            'returnDate': end_date,
            'durationOfStay': minimal_duration,
            'adults': 2,
            'currencyCode': 'PLN',
            'max': 50
        }

        fs = FlightSearch()

        fs.flight_search(flight_data)

        # Open the results dialog
        self.results_dialog = ResultsDialog(fs.search_result)
        self.results_dialog.exec()


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Date')

        self.layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        self.layout.addWidget(self.calendar)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        self.selected_date = None

    def accept(self):
        self.selected_date = self.calendar.selectedDate()
        super().accept()
