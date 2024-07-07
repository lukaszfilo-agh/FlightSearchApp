from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog
)


class DestinationsResultDialog(QDialog):
    """
    Class used for displaying window with destinations results
    """

    def __init__(self, api_response, origin, parent=None):
        super().__init__(parent)
        self.initUI(api_response, origin)

    def initUI(self, api_response, origin):
        """
        Function responsible for initializing GUI for Destinations Results Dialog
        """
        self.setWindowTitle('Destinations Search Results')
        self.resize(500, 800)

        layout = QVBoxLayout()

        self.origin_label = QLabel()
        self.origin_label.setText(f"Origin: {origin}")
        layout.addWidget(self.origin_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(1)
        self.results_table.setHorizontalHeaderLabels(['City'])
        self.results_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.results_table.resizeColumnsToContents()
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setStyleSheet(
            "alternate-background-color: #4a4a4a; background-color: #272727;")
        layout.addWidget(self.results_table)

        self.setLayout(layout)
        self.show_results(api_response)

    def show_results(self, api_response):
        """
        Function responsible for showing results from API response
        """
        # Clear previous results
        self.results_table.setRowCount(0)
        self.results_table.setRowCount(len(api_response))
        for row, dest in enumerate(api_response):
            city = dest['arrivalAirport']['city']['name']
            self.results_table.setItem(row, 0, QTableWidgetItem(city))
