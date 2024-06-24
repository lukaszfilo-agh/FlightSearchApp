from PyQt6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QMenu
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QClipboard
from datetime import datetime


class ResultsDialog(QDialog):
    def __init__(self, api_response, search_engine, parent=None):
        super().__init__(parent)
        self.search_engine = search_engine
        if self.search_engine == 'Amadeus':
            self.initUI_amadeus(api_response)
        elif self.search_engine == 'Ryanair':
            self.initUI_ryanair(api_response)

    def initUI_amadeus(self, api_response):
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

        self.results_table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(
            self.show_context_menu)

        self.setLayout(layout)
        self.display_results_amadeus(api_response)

    def initUI_ryanair(self, api_response):
        self.setWindowTitle('Flight Search Results')
        self.resize(1400, 800)

        layout = QVBoxLayout()

        self.origin_label = QLabel()
        origin = api_response['fares'][0]['outbound']['departureAirport']['name']
        self.origin_label.setText(f"Origin: {origin}")
        layout.addWidget(self.origin_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(9)
        self.results_table.setHorizontalHeaderLabels(['Flight Numbers', 'Destination', 'Outbound date', 'Departure time',
                                                     'Arrival time', 'Inbound date', 'Departure time',
                                                      'Arrival time', 'Price'])
        self.results_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.results_table.resizeColumnsToContents()
        layout.addWidget(self.results_table)

        self.results_table.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(
            self.show_context_menu)

        self.setLayout(layout)
        self.display_results_ryanair(api_response)

    def show_context_menu(self, position):
        menu = QMenu()
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy_selection)
        menu.addAction(copy_action)
        menu.exec(self.results_table.viewport().mapToGlobal(position))

    def copy_selection(self):
        selection = self.results_table.selectedIndexes()
        if selection:
            rows = sorted(set(index.row() for index in selection))
            columns = sorted(set(index.column() for index in selection))

            copy_text = ""
            for row in rows:
                row_data = []
                for column in columns:
                    index = self.results_table.item(row, column)
                    if index:
                        row_data.append(index.text())
                copy_text += "\t".join(row_data) + "\n"

            clipboard = QApplication.clipboard()
            clipboard.setText(copy_text.strip())

    def display_results_amadeus(self, api_response):
        # Clear previous results
        self.results_table.setRowCount(0)
        if 'data' in api_response and api_response['data']:
            flight_data = api_response['data']

            self.results_table.setRowCount(len(flight_data))

            for row, flight in enumerate(flight_data):
                flight_number = ", ".join(segment['carrierCode'] + segment['number']
                                          for segment in flight['itineraries'][0]['segments'])
                departure_time = flight['itineraries'][0]['segments'][0]['departure']['at']
                arrival_time = flight['itineraries'][0]['segments'][-1]['arrival']['at']
                duration = flight['itineraries'][0]['duration']
                price = flight['price']['grandTotal'] + \
                    " " + flight['price']['currency']

                self.results_table.setItem(
                    row, 0, QTableWidgetItem(flight_number))
                self.results_table.setItem(
                    row, 1, QTableWidgetItem(departure_time))
                self.results_table.setItem(
                    row, 2, QTableWidgetItem(arrival_time))
                self.results_table.setItem(row, 3, QTableWidgetItem(duration))
                self.results_table.setItem(row, 4, QTableWidgetItem(price))
        else:
            # Display no results message
            self.results_table.setRowCount(1)
            no_results_item = QTableWidgetItem('No flights found.')
            no_results_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(0, 0, no_results_item)

    def display_results_ryanair(self, api_response):
        # Clear previous results
        self.results_table.setRowCount(0)
        if 'fares' in api_response and api_response['fares']:
            flight_data = api_response['fares']

            self.results_table.setRowCount(len(flight_data))

            for row, fare in enumerate(flight_data):
                flight_numbers = f"{fare['outbound']['flightNumber']} {fare['inbound']['flightNumber']}"
                destination = fare['outbound']['arrivalAirport']['name']
                out_date = datetime.fromisoformat(
                    fare['outbound']['departureDate']).strftime('%d.%m.%Y')
                out_dep_time = datetime.fromisoformat(
                    fare['outbound']['departureDate']).strftime('%H:%M')
                out_arr_time = datetime.fromisoformat(
                    fare['outbound']['arrivalDate']).strftime('%H:%M')
                in_date = datetime.fromisoformat(
                    fare['inbound']['departureDate']).strftime('%d.%m.%Y')
                in_dep_time = datetime.fromisoformat(
                    fare['inbound']['departureDate']).strftime('%H:%M')
                in_arr_time = datetime.fromisoformat(
                    fare['inbound']['arrivalDate']).strftime('%H:%M')
                price = f"{fare['summary']['price']['value']}{fare['summary']['price']['currencyCode']}"

                self.results_table.setItem(
                    row, 0, QTableWidgetItem(flight_numbers))
                self.results_table.setItem(
                    row, 1, QTableWidgetItem(destination))
                self.results_table.setItem(
                    row, 2, QTableWidgetItem(out_date))
                self.results_table.setItem(
                    row, 3, QTableWidgetItem(out_dep_time))
                self.results_table.setItem(
                    row, 4, QTableWidgetItem(out_arr_time))
                self.results_table.setItem(
                    row, 5, QTableWidgetItem(in_date))
                self.results_table.setItem(
                    row, 6, QTableWidgetItem(in_dep_time))
                self.results_table.setItem(
                    row, 7, QTableWidgetItem(in_arr_time))
                self.results_table.setItem(row, 8, QTableWidgetItem(price))
        else:
            # Display no results message
            self.results_table.setRowCount(1)
            no_results_item = QTableWidgetItem('No flights found.')
            no_results_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(0, 0, no_results_item)
