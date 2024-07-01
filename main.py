import sys

from PyQt6.QtWidgets import QApplication

from FlightSearchApp import FlightSearchApp


def main():
    app = QApplication(sys.argv)
    ex = FlightSearchApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
