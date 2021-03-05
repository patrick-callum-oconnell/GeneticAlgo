"""
This file will be the new driver. The buttons and sliders in the GUI will control the old command line arguments
that will be passed to the old driver which takes in command line arguments and runs the algorithm.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

window = QWidget()
window.show()

app.exec()