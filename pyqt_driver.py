"""
This file will be the new driver. The buttons and sliders in the GUI will control the old command line arguments
that will be passed to the old driver which takes in command line arguments and runs the algorithm.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)
app.setStyle('Fusion')



class SliderWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(SliderWindow, self).__init__(*args, **kwargs)

        layout = QHBoxLayout()

        self.setWindowTitle("Genetic Algorithm Visualizer 1.0")

        label = QLabel("Set Population Size (range 0 to 10000):")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

        pop_size = QSlider(Qt.Horizontal)
        pop_size.setTickPosition(QSlider.TicksBelow)
        pop_size.setTickInterval(10)

        layout.addWidget(pop_size)

        self.setLayout(layout)

window = SliderWindow()
window.show()

app.exec()