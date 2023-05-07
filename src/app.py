from PyQt5.QtWidgets import(
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QMainWindow,
    QFileDialog,
    QLabel
)

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QT_VERSION_STR

import pyqtgraph as pg

import warnings
warnings.filterwarnings("ignore")

'''
    ComboBox that can add entries from a given list
'''
class QIComboBox(QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)

'''
    Application window
'''
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Distribution from derivative")

        # list of the distributions to fit
        list_dist = [
            "Cauchy",
            "Gauss",
        ]

        # the layouts
        layout1 = QHBoxLayout() # for the plot
        layout2 = QHBoxLayout() # for the buttons

        # variables
        self.file = None
        self.x_vals = None
        self.y_vals = None

        '''
            Buttons
        '''
        # Load file button
        self.button_load = QPushButton("Load data-points")
        self.button_load.clicked.connect(self.read_datapoints)
        self.button_load.setToolTip("Load data-points")

        # Load derivative data
        self.button_load = QPushButton("Load derivatives")
        self.button_load.clicked.connect(self.read_datapoints)
        self.button_load.setToolTip("Load the pre-determined derivatives stored in a file.")
        
        # Get derivatives of the input data?
        self.button_deriv = QPushButton("Find derivative")
        self.button_deriv.clicked.connect(self.get_derivative)
        self.button_deriv.setToolTip("If the data-points have very short x-step, one can approximate the derivative using this button.")

        # Choose a distribution to fit over
        self.combo_box = QIComboBox()
        for option in list_dist:
            self.combo_box.addItem(option)
        self.button_load.setToolTip("Load the pre-determined derivatives stored in a file.")


        # graphing area
        size_ratio = 4
        self.plotter = pg.PlotWidget() # the plotting widget
        self.plotter.setBackground('w') # white background
        self.plot_item = self.plotter.getPlotItem() # the plot item

        '''
            Layout info
        '''
        # button layout
        layout2.addWidget(self.button_load)
        layout2.addWidget(self.button_deriv)
        layout2.addWidget(self.button_save)
        # the entire layout
        layout1.addWidget(self.plotter, size_ratio)
        layout1.addLayout(layout2)

        # copyright line
        dev = QLabel("Bug reports to the developer at: han_kyunghoon@naver.com -- © Kyunghoon Han")
        layout1.addWidget(dev)


    def button_load(self):
        '''
            button_load
        '''
        return None
    
    def button_deriv(self):
        '''
            button_deriv
        '''
        return None
    
    def button_save(self):
        '''
            button_save
        '''
        return None