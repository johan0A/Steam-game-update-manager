from PyQt5.QtWidgets import QApplication
from ui.main_window import Main_window
import sys

# activate more debug output
import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    app = QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec_())

main()