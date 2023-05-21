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
import numpy as np

from os.path import abspath
from pathlib import Path

from scipy.signal import find_peaks
from utils.fitter import Interpolate
from utils.cauchy import get_cauchy

import warnings, sys, os
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
        layout_whole = QVBoxLayout() # for the Dev Note
        layout0 = QHBoxLayout() # for the whole thing
        layout1 = QVBoxLayout() # for the plotting space
        layout2 = QHBoxLayout() # for the buttons
        layout3 = QVBoxLayout() # for the controls

        # variables
        self.file = None
        self.x_vals = None
        self.y_vals = None
        self.x_peaks= None
        self.y_peaks= None
        self.y_diff = None
        self.peak_indices = []
        self.list_plots = []

        '''
            Buttons
        '''
        # Load file button
        self.button_load = QPushButton("Load data-points")
        self.button_load.clicked.connect(self.read_datapoints)
        self.button_load.setToolTip("Load data-points")

        # Run algorithm button
        self.button_run = QPushButton("Run algorithm")
        self.button_run.clicked.connect(self.run_algorithm)
        self.button_run.setToolTip("Run the algorithm")

        # Get derivatives of the input data?
        self.button_save = QPushButton("Save peak info")
        self.button_save.clicked.connect(self.save_peaks)
        self.button_save.setToolTip("Save peak information.")

        # Choose a distribution to fit over
        self.dist_combo_box = QIComboBox()
        for option in list_dist:
            self.dist_combo_box.addItem(option)

        # Draw the distributions over
        self.dist_button = QPushButton("Draw distributions")
        self.dist_button.clicked.connect(self.draw_dist)
        self.dist_button.setToolTip("Draw the distributions over the plot.")
        
        # Button to find peaks
        self.peak_button = QPushButton("Find Peaks")
        self.peak_button.clicked.connect(self.find_peaks)
        self.peak_button.setToolTip("Push this to find the peaks")

        # Clear plot
        self.button_clear = QPushButton("Clear Plots")
        self.button_clear.clicked.connect(self.clear_plot)
        self.button_clear.setToolTip("Clear the plot with this button")

        # graphing area
        size_ratio = 4
        self.plotter = pg.PlotWidget() # the plotting widget
        self.plotter.setBackground('w') # white background
        self.plot_item = self.plotter.getPlotItem() # the plot item

        '''
            Layout info
        '''
        # the entire layout
        layout1.addWidget(self.plotter, size_ratio)
        layout1.addLayout(layout2)
        # the controls
        layout3.addWidget(self.button_load)
        layout3.addWidget(self.peak_button)
        layout3.addWidget(self.dist_combo_box)
        layout3.addWidget(self.dist_button)
        layout3.addWidget(self.button_run)
        layout3.addWidget(self.button_save)
        layout3.addWidget(self.button_clear)
        # the whole thing
        layout0.addLayout(layout1)
        layout0.addLayout(layout3)

        # copyright line
        dev = QLabel("Bug reports to the developer at: han_kyunghoon@naver.com -- © Kyunghoon Han")
        layout_whole.addLayout(layout0)
        layout_whole.addWidget(dev)

        # define the main layout
        main_widget = QWidget()
        main_widget.setLayout(layout_whole)
        self.setCentralWidget(main_widget)

    def clear_plot(self):
        '''
            clears the plot
        '''
        self.plotter.clear()
        self.list_plots = []

    def read_datapoints(self):
        '''
            read_datapoints
        '''
        dir_path = str(abspath(os.getcwd()))
        self.file, _ = QFileDialog.getOpenFileName(
            self,
            'Select a file to import',
            dir_path,
            'Files (*.csv, *.txt)'
        )
        if self.file is None:
            return None # change it when self.plot() is defined
        elif self.file is not None:
            if "csv" in self.file[-4:] or "txt" in self.file[-4:]:
                try:
                    arr = np.loadtxt(self.file, delimiter=',')
                except ValueError:
                    try:
                        arr = np.loadtxt(self.file, delimiter=' ')
                    except ValueError:
                        arr = np.loadtxt(self.file, delimiter='\t')
        interpolation_obj = Interpolate(
                                arr[:,0], arr[:,1],
                                degree_spline=3,
                                gratings=1000)
        self.x_vals = interpolation_obj.x_val
        self.y_vals = interpolation_obj.y_val
        self.y_diff = interpolation_obj.first_deriv

        # then plot the data here
        self.plot_input_data()
        return None
    
    def plot_input_data(self):
        self.plotter.clear()
        # cache the data
        self.x_orig = self.x_vals
        self.y_orig = self.y_vals
        # then plot
        plot_item = self.plotter.plot(
            self.x_vals, self.y_vals, connect="finite",
            pen=pg.mkPen(width=5)
        )
        self.list_plots.append(plot_item)  # list of line plots here

        if self.file is None:
            self.plotter.setLabels(title="The title goes here")
        else:
            self.plotter.setTitle(title="Some spectral data", size='20px')
        self.plotter.setLabel('left',"Intensity", size='20px', color='#808080')
        self.plotter.setLabel('bottom',"Wavenumber (cmᐨ¹)", size='20px', color='#808080')
        self.plotter.setContentsMargins(0, 0, 0, 0)
    
    def run_algorithm(self):
        '''
            run_algorithm (button)
        '''
        return None
    
    def save_peaks(self):
        '''
            save_peaks (button)
        '''
        return None
    
    def draw_dist(self):
        """
            draw_dist
        """
        if self.dist_combo_box.currentText() == "Cauchy":
            list_cauchies = get_cauchy(self.x_vals, 
                                       self.y_vals,
                                       self.y_diff,
                                       self.peak_indices)
            for cauchy in list_cauchies:
                print(cauchy)
                print(type(cauchy))
                plot_item = self.plotter.plot(
                    self.x_vals, cauchy, connect="finite",
                    pen=pg.mkPen(width=5, color=(30, 30, 200)))
                self.list_plots.append(plot_item)
        elif self.dist_combo_box.currentText() == "Gauss":
            return None
        return None
    
    def find_peaks(self):
        '''
            find_peaks
        '''
        self.peak_indices, _ = find_peaks(self.y_vals)
        self.peak_indices = self.peak_indices.tolist()
        self.x_peaks = self.x_vals[self.peak_indices]
        self.y_peaks = self.y_vals[self.peak_indices]
        plot_item = self.plotter.plot(
            self.x_peaks, self.y_peaks, connect="finite",
            pen=None, symbol='x'
        )
        self.list_plots.append(plot_item)  # list of line plots here
        return None

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()