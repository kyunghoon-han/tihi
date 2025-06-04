from PyQt5.QtWidgets import(
    QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout,
    QPushButton,
)
from PyQt5.QtWidgets import QWizardPage, QComboBox
import pyqtgraph as pg
from tihi.tihi_utils.interpolate import Interpolate
import numpy as np

class InterpolationPage(QWizardPage):
    '''
    Wizard page for interpolating and denoising data.

    x_vals         : Input x-axis values.
    y_vals         : Input y-axis values.
    x_label        : Label for the x-axis.
    y_label        : Label for the y-axis.
    title          : Title for the plot.
    '''
    def __init__(self, x_vals, y_vals, x_label="x-axis", y_label="y-axis", title="title"):
        super(InterpolationPage, self).__init__()
        self.inblp = True
        # input x and y values & smoothness parameter
        self.x_orig = x_vals # non-interpolated values
        self.y_orig = y_vals # these are stored in case the baseline
                             # correction needs to be done again
        self.num_points              = len(self.x_orig)
        self.x_vals                  = x_vals
        self.y_vals                  = y_vals
        
        # graphing tools
        self.plotter = pg.PlotWidget() # the plotting widget
        self.plotter.setBackground('w') # white background
        self.plotter.plot(self.x_vals, self.y_vals)
        self.textbox_title  = QLineEdit(title)
        self.textbox_xlabel = QLineEdit(x_label)
        self.textbox_ylabel = QLineEdit(y_label)
        
        #self.interpolate_data()

        # GUI Layouts
        self.layout1                  = QHBoxLayout()
        self.layout2                  = QVBoxLayout()
        self.buttons_layout1          = QHBoxLayout()
        self.buttons_layout2          = QHBoxLayout()
        # text components
        self.label_numpoints          = QLabel()
        self.label_window_denoise     = QLabel()
        self.label_numpoints.setText("Number of points")
        self.label_window_denoise.setText("Denoise window size")
        self.text_numpoints           = QLineEdit("100")
        self.text_denoise_window_size = QLineEdit("10")
        self.text_numpoints.textChanged.connect(self.change_numpoints)
        self.text_denoise_window_size.textChanged.connect(self.change_denoise_window_size)
        self.change_numpoints()
        self.change_denoise_window_size()
        self.button_denoise           = QPushButton("Denoise")
        self.button_interpolate       = QPushButton("Interpolate")
        self.button_clear             = QPushButton("Clear")
        self.next_button              = QPushButton("Next")
        self.button_denoise.clicked.connect(self.denoise)
        self.button_interpolate.clicked.connect(self.interpolate_data)
        self.button_clear.clicked.connect(self.clear)
        #self.next_button.clicked.connect(self.next)
        
        # set the layout inputs
        self.layout1.addWidget(self.plotter)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.label_numpoints)
        self.layout2.addWidget(self.text_numpoints)
        self.layout2.addWidget(self.label_window_denoise)
        self.layout2.addWidget(self.text_denoise_window_size)
        self.layout2.addLayout(self.buttons_layout1)
        self.buttons_layout1.addWidget(self.button_interpolate)
        self.buttons_layout1.addWidget(self.button_denoise)
        self.layout2.addLayout(self.buttons_layout2)
        self.buttons_layout2.addWidget(self.button_clear)
        
        self.setLayout(self.layout1)
        
        # plot initial stuff
        self.plot_input_data()
        
    def change_numpoints(self):
        '''
        Updates the number of points to use for interpolation based on user input.
        '''
        self.num_points = int(self.text_numpoints.text())
    
    def change_denoise_window_size(self):
        '''
        Updates the denoise window size based on user input.
        '''
        self.denoise_window = int(self.text_denoise_window_size.text())

    def denoise(self):
        '''
        Denoises the interpolated data and updates the plot.
        '''
        self.interpolate_data()
        self.interpolated.denoise_signal()
        self.x_vals = self.interpolated.x_val
        self.y_vals = self.interpolated.y_val
        self.plot_input_data(denoise=True)
        
    def interpolate_data(self):
        '''
        Interpolates the original data and updates the plot.
        '''
        self.initial = True
        self.interpolated = Interpolate(self.x_vals, self.y_vals,gratings=self.num_points)
        self.x_vals = self.interpolated.x_val
        self.y_vals = self.interpolated.y_val
        self.plot_input_data()
    
    def clear(self):
        '''
        Clears the plot and re-plots the original data.
        '''
        self.plotter.clear()
        self.num_points = len(self.x_orig)
        self.x_vals = self.x_orig
        self.y_vals = self.y_orig
        # Instead of re-interpolating and plotting, just plot the original data
        self.plotter.plot(
            self.x_vals, self.y_vals, connect="finite",
            pen=pg.mkPen(width=5)
        )
        
    def plot_input_data(self, denoise=False):
        '''
        Plots the input data.

        denoise: If True, plot with denoising (green line).
        '''
        # then plot
        if not denoise:
            plot_item = self.plotter.plot(
                self.x_vals, self.y_vals, connect="finite",
                pen=pg.mkPen(width=5)
            )
        else:
            plot_item = self.plotter.plot(
                self.x_vals, self.y_vals, connect="finite",
                pen=pg.mkPen(color=(0,255,0), width=5)
            )
        self.plotter.setContentsMargins(0, 0, 0, 0)
