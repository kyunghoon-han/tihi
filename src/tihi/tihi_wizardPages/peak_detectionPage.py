from PyQt5.QtWidgets import(
    QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout,
    QPushButton,
)
from PyQt5.QtWidgets import QWizardPage, QComboBox
import pyqtgraph as pg
from tihi.tihi_utils.peak_detection import find_peaks
import numpy as np

class PeakDetectionPage(QWizardPage):
    def __init__(self, interpolation_class, x_label="x-axis", y_label="y-axis", title="title"):
        super(PeakDetectionPage, self).__init__()
        
        self.interpolation_class = interpolation_class
        self.peak_indices        = []
        self.window_size         = 10
        self.threshold           = 0.1
        self.min_amps            = 0.0
        
        # GUI Layouts
        self.layout1                  = QHBoxLayout()
        self.layout2                  = QVBoxLayout()
        # text components
        self.label_window_size        = QLabel()
        self.minimum_amplitude        = QLabel()
        self.label_threshold          = QLabel()
        self.label_window_size.setText("Window size for peak detection:")
        self.minimum_amplitude.setText("Minimum amplitude (default : 0.0)")
        self.label_threshold.setText("Threshold (default: 0.05)")
        self.window_size_edit         = QLineEdit("10")
        self.min_amp_edit             = QLineEdit("0.0")
        self.threshold_edit           = QLineEdit("0.05")
        self.button_run               = QPushButton("Detect Peaks")
        self.button_clear             = QPushButton("Clear plot")
        
        # functions
        self.window_size_edit.textChanged.connect(self.window_size_changes)
        self.threshold_edit.textChanged.connect(self.threshold_changes)
        self.min_amp_edit.textChanged.connect(self.min_amp_changes)
        self.button_run.clicked.connect(self.run)
        self.button_clear.clicked.connect(self.clear)
        
        
        # graphing tools
        self.plotter = pg.PlotWidget() # the plotting widget
        self.plotter.setBackground('w') # white background
        self.plotter.plot(interpolation_class.x_val, interpolation_class.y_val)
        self.textbox_title  = QLineEdit(title)
        self.textbox_xlabel = QLineEdit(x_label)
        self.textbox_ylabel = QLineEdit(y_label)
        
        # set the layout inputs
        self.layout1.addWidget(self.plotter)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.label_window_size)
        self.layout2.addWidget(self.window_size_edit)
        self.layout2.addWidget(self.minimum_amplitude)
        self.layout2.addWidget(self.min_amp_edit)
        self.layout2.addWidget(self.label_threshold)
        self.layout2.addWidget(self.threshold_edit)
        self.layout2.addWidget(self.button_run)
        self.layout2.addWidget(self.button_clear)
        
        self.setLayout(self.layout1)
        
        # plot initial stuff
        self.plot_input_data()
    
    def run(self):
        self.peak_indices = find_peaks(self.interpolation_class, 
                                  window_size=self.window_size,
                                  threshold=self.threshold,
                                  min_amp=self.min_amps)
        self.plot_input_data(peak=True)
        
    
    def window_size_changes(self):
        self.window_size = int(self.window_size_edit.text())
    
    def threshold_changes(self):
        self.threshold = float(self.threshold_edit.text())
        
    def min_amp_changes(self):
        self.min_amps  = float(self.min_amp_edit.text())
    
    def plot_input_data(self, peak=False):
        """Plot the input data called by the self.read_file function
        """
        self.plotter.clear()
        # then plot
        plot_item = self.plotter.plot(
            self.interpolation_class.x_val, self.interpolation_class.y_val, connect="finite",
            pen=pg.mkPen(width=5)
        )
        if peak:
            self.plotter.plot(
                self.interpolation_class.x_val[self.peak_indices],
                self.interpolation_class.y_val[self.peak_indices],
                pen=None,
                name="BEP",
                symbol='o',
                symbolPen=pg.mkPen(color=(0, 0, 255), width=0),                                      
                symbolBrush=pg.mkBrush(0, 0, 255, 255),
                symbolSize=7)
        self.plotter.setContentsMargins(0, 0, 0, 0)
        
    def clear(self):
        self.plotter.clear()