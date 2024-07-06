from PyQt6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QMenu
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QClipboard
from datetime import datetime

# Color price cell according to price


class ResultsDialog(QDialog):
    def __init__(self, api_response, parent=None):
        super().__init__(parent)
        self.initUI_ryanair(api_response)

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
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setStyleSheet(
            "alternate-background-color: #4a4a4a; background-color: #272727;")

        # Enable sorting
        self.results_table.setSortingEnabled(True)
        self.results_table.horizontalHeader().setSortIndicatorShown(True)
        self.results_table.horizontalHeader().setSectionsClickable(True)

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
                price_value = fare['summary']['price']['value']
                price_currency = fare['summary']['price']['currencyCode']
                price = f"{price_value}{price_currency}"

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
                
                price_item = QTableWidgetItem(price)
                price_item.setData(Qt.ItemDataRole.UserRole, price_value)
                self.results_table.setItem(row, 8, price_item)
        else:
            # Display no results message
            self.results_table.setRowCount(1)
            no_results_item = QTableWidgetItem('No flights found.')
            no_results_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_table.setItem(0, 0, no_results_item)
