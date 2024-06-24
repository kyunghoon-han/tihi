from PyQt5.QtWidgets import(
    QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout,
    QPushButton,
)
from PyQt5.QtWidgets import QWizardPage, QComboBox
import pyqtgraph as pg
from tihi.tihi_utils.baseline_corrector import (linear_baseline_correction, airPLS, arPLS)
import numpy as np

class QIComboBox(QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)

class BaselinePage(QWizardPage):
    def __init__(self, x_vals, y_vals, x_label="x-axis", y_label="y-axis", title="title"):
        super(BaselinePage, self).__init__()
        self.inblp = True
        # input x and y values & smoothness parameter
        self.x_orig = x_vals # non-interpolated values
        self.y_orig = y_vals # these are stored in case the baseline
                             # correction needs to be done again
        self.num_points              = len(self.x_orig)
        self.x_vals                  = x_vals
        self.y_vals                  = y_vals
        
        # variables
        self.method                  = None
        self.ratio                   = 1e-6
        self.lambda_param            = 100
        self.baseline                = None
        
        # graphing tools
        self.plotter = pg.PlotWidget() # the plotting widget
        self.plotter.setBackground('w') # white background
        self.plotter.plot(self.x_vals, self.y_vals)
        self.textbox_title  = QLineEdit(title)
        self.textbox_xlabel = QLineEdit(x_label)
        self.textbox_ylabel = QLineEdit(y_label)
        
        list_methods=["None", "Linear", "arPLS", "airPLS"]
        
        # GUI Layouts
        self.layout1                  = QHBoxLayout()
        self.layout2                  = QVBoxLayout()
        self.buttons_layout1          = QHBoxLayout()
        # text components
        self.label_method_name        = QLabel()
        self.label_lambda             = QLabel()
        self.label_method_name.setText("Baseline correction method:")
        self.label_lambda.setText("Parameter for PLS methods (default: 100)")
        self.label_ratio              = QLabel()
        self.label_ratio.setText("Ratio for arPLS (default: 1e-6)")
        self.method_combobox          = QIComboBox()
        self.lambda_val               = QLineEdit("200")
        self.ratio_val                = QLineEdit("0.0000006")
        for option in list_methods:
            self.method_combobox.addItem(option)
        self.method_combobox.activated.connect(self.method_changes)
        self.button_run               = QPushButton("Detrend")
        self.button_clear             = QPushButton("Clear plot")
        
        # functions
        self.lambda_val.textChanged.connect(self.lambda_changes)
        self.ratio_val.textChanged.connect(self.ratio_changes)
        self.button_run.clicked.connect(self.run)
        self.button_clear.clicked.connect(self.clear)
        
        # set the layout inputs
        self.layout1.addWidget(self.plotter)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.label_method_name)
        self.layout2.addWidget(self.method_combobox)
        self.layout2.addWidget(self.label_lambda)
        self.layout2.addWidget(self.lambda_val)
        self.layout2.addWidget(self.label_ratio)
        self.layout2.addWidget(self.ratio_val)
        self.layout2.addLayout(self.buttons_layout1)
        self.buttons_layout1.addWidget(self.button_run)
        self.buttons_layout1.addWidget(self.button_clear)
        
        self.setLayout(self.layout1)
        
        # plot initial stuff
        self.plot_input_data()
    
    def ratio_changes(self):
        self.ratio = float(self.ratio_val.text())
    
    def lambda_changes(self):
        self.lambda_param = float(self.lambda_val.text())
    
    def method_changes(self):
        self.method = str(self.method_combobox.currentText())
    
    def run(self):
        self.clear() # clear the plot first
        if self.method is None:
            pass
        elif self.method == "None":
            pass
        elif self.method == "Linear":
            self.baseline = linear_baseline_correction(self.x_vals, self.y_vals)
            self.y_vals    = self.y_orig - self.baseline
        elif self.method == "airPLS":
            self.baseline = airPLS(self.y_vals, self.lambda_param)
            self.y_vals    = self.y_orig - self.baseline
        elif self.method == "arPLS":
            self.baseline = arPLS(self.y_vals, self.ratio, self.lambda_param)
            self.y_vals    = self.y_orig - self.baseline
        else:
            print("something's wrong")
            return None
        self.plot_input_data()
    
    def clear(self):
        self.plotter.clear()
        self.num_points              = len(self.x_orig)
        self.x_vals                  = self.x_orig
        self.y_vals                  = self.y_orig
        self.baseline                = None
        self.plot_input_data()
        
    def plot_input_data(self):
        """Plot the input data called by the self.read_file function
        """
        # then plot
        plot_item = self.plotter.plot(
            self.x_orig, self.y_orig, connect="finite",
            pen=pg.mkPen(width=5)
        )
        if self.baseline is not None:
            self.plotter.plot(
                self.x_vals, self.y_vals, connect="finite",
                pen=pg.mkPen(color=(0, 0, 255), width=5)
            )
            self.plotter.plot(
                self.x_vals, self.baseline, connect="finite",
                pen=pg.mkPen(color=(0,255,0), wdith=5)
            )
        self.plotter.setContentsMargins(0, 0, 0, 0)