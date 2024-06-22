import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QComboBox, QCalendarWidget, QListWidget, QSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt

from flight_search import FlightSearch


class ResultsDialog(QDialog):
    def __init__(self, api_response, parent=None):
        super().__init__(parent)
        self.initUI(api_response)

    def initUI(self, api_response):
        self.setWindowTitle('Flight Search Results')
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(
            ['Flight', 'Departure', 'Arrival', 'Duration', 'Price'])
        self.results_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.results_table)

        self.setLayout(layout)

        self.display_results(api_response)

    def display_results(self, api_response):
        # Clear previous results
        self.results_table.setRowCount(0)
        if 'data' in api_response and api_response['data']:
            flight_data = api_response['data']
            dictionaries = api_response['dictionaries']

            self.results_table.setRowCount(len(flight_data))
            
            for row, flight in enumerate(flight_data):
                flight_number = ", ".join(segment['carrierCode'] + segment['number']
                                        for segment in flight['itineraries'][0]['segments'])
                departure_time = flight['itineraries'][0]['segments'][0]['departure']['at']
                arrival_time = flight['itineraries'][0]['segments'][-1]['arrival']['at']
                duration = flight['itineraries'][0]['duration']
                price = flight['price']['grandTotal'] + \
                    " " + flight['price']['currency']

                self.results_table.setItem(row, 0, QTableWidgetItem(flight_number))
                self.results_table.setItem(
                    row, 1, QTableWidgetItem(departure_time))
                self.results_table.setItem(row, 2, QTableWidgetItem(arrival_time))
                self.results_table.setItem(row, 3, QTableWidgetItem(duration))
                self.results_table.setItem(row, 4, QTableWidgetItem(price))
        # if 'data' in api_response and api_response['data']:
        #     for idx, flight in enumerate(api_response['data']):
        #         # Extract relevant information from the flight data
        #         flight_id = flight['id']
        #         departure_time = flight['itineraries'][0]['segments'][0]['departure']['at']
        #         arrival_time = flight['itineraries'][0]['segments'][-1]['arrival']['at']
        #         duration = flight['itineraries'][0]['duration']
        #         price = flight['price']['total']

        #         # Populate table rows with flight details
        #         self.results_table.insertRow(idx)
        #         self.results_table.setItem(idx, 0, QTableWidgetItem(flight_id))
        #         self.results_table.setItem(
        #             idx, 1, QTableWidgetItem(departure_time))
        #         self.results_table.setItem(
        #             idx, 2, QTableWidgetItem(arrival_time))
        #         self.results_table.setItem(idx, 3, QTableWidgetItem(duration))
        #         self.results_table.setItem(idx, 4, QTableWidgetItem(price))

        #         # Resize columns to content
        #         self.results_table.resizeColumnsToContents()
        else:
            # Display no results message
            self.results_table.setRowCount(1)
            no_results_item = QTableWidgetItem('No flights found.')
            no_results_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(0, 0, no_results_item)


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

        # Search Engine Selection
        engine_layout = QHBoxLayout()
        engine_label = QLabel('Search Engine:')
        self.engine_selection = QComboBox()
        # Add more options if needed
        self.engine_selection.addItems(['Amadeus', 'Ryanair'])
        engine_layout.addWidget(engine_label)
        engine_layout.addWidget(self.engine_selection)

        # Search Button
        self.search_button = QPushButton('Search Flights')
        self.search_button.clicked.connect(self.search_flights)

        # Add all layouts to the main layout
        main_layout.addLayout(engine_layout)
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
        self.resize(800, 600)

    def add_destination(self):
        destination = self.destination_input.text()
        if destination:
            self.destination_list.addItem(destination)
            self.destination_input.clear()

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
        duration = self.duration_input.value()
        travel_class = self.class_selection.currentText()
        search_engine = self.engine_selection.currentText()  # Get selected search engine

        flight_data = {
            'origin': origin,
            'originLocationCode': [],
            'destination': destinations,
            'destinationLocationCode': [],
            'departureDate': start_date,
            'returnDate': end_date,
            'durationOfStay': duration,
            'adults': 2,
            'currencyCode': 'PLN',
            'max': 50
        }

        fs = FlightSearch()

        if search_engine == 'Amadeus':

            fs.flight_search_amadeus(flight_data)

            results = fs.search_result

        elif search_engine == 'Ryanair':
            fs.flight_search_ryanair(flight_data)
            results = fs.search_result
        else:
            return
        
        # Open the results dialog
        self.results_dialog = ResultsDialog(results)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlightSearchApp()
    ex.show()
    sys.exit(app.exec())
