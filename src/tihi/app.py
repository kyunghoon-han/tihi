#!/usr/bin/env python

import sys, os
import numpy as np
from os.path import abspath
from tihi.wizard import MagicWizard
import ctypes

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QMainWindow,
    QFileDialog, QWizard, QLabel,
    QSystemTrayIcon
)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QT_VERSION_STR

import pyqtgraph as pg

import warnings
warnings.filterwarnings("ignore")

print("Imported PyQt version : ", QT_VERSION_STR)

class WizardWindow(QMainWindow):
    def __init__(self, x_vals, y_vals,x_label, y_label, title):
        """Wizard window class

        Args:
            x_vals (np array): x-values of the signal
            y_vals (np array): y-values of the signal
        """
        super().__init__()
        
        # initial stuff
        self.approximation  = None
        self.decompositions = []
        self.params         = []
        self.dist_type      = None
        
        self.wizard = MagicWizard(x_vals, y_vals, x_label, y_label, title)
        self.setCentralWidget(self.wizard)
        self.wizard.button(QWizard.FinishButton).clicked.connect(self.closure)
        # Disable the back button on initialization
        self.wizard.button(QWizard.BackButton).hide()
    
    def closure(self):
        self.dist_type = self.wizard.distribution.distribution_type
        if self.dist_type is not None:
            self.approximation  = self.wizard.distribution.approximation
            self.decompositions = self.wizard.distribution.decompositions
            self.params         = self.wizard.distribution.params
        self.close()
        

"""
    Main window of the application
"""
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tihi spectral peak finder / analyser")
        
        my_app_id = "tihi.1.0.0"
        # to let Windows know if the 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
        
        icon_path = "src/tihi/logo_small.png"
        icon_obj = QIcon()
        icon_obj.addFile('src/tihi/icons/16.png', QSize(16,16))
        icon_obj.addFile('src/tihi/icons/32.png', QSize(32,32))
        icon_obj.addFile('src/tihi/icons/64.png', QSize(64,64))
        icon_obj.addFile('src/tihi/icons/128.png', QSize(128,128))
        icon_obj.addFile('src/tihi/icons/256.png', QSize(256,256))
        self.setWindowIcon(icon_obj)
        
        tray = QSystemTrayIcon()
        tray.setIcon(icon_obj)
        tray.setVisible(True)

        # initialization of the variables
        self.file     = None
        self.x_vals   = None    # data for the modified signal
        self.y_vals   = None
        self.x_orig   = None    # data for the original signal
        self.y_orig   = None
        
        self.params   = None
        
        # define the buttons
        self.button_load = QPushButton("Load File")
        self.button_load.clicked.connect(self.read_file)
        self.button_load.setToolTip("Load a file where the first column is the x-values and the second column is the y-values")
        
        self.button_run = QPushButton("Run")
        self.button_run.setToolTip("Run the wizard that guides the users to apply the peak detection and fitting algorithms")
        self.button_run.clicked.connect(self.run_wizard)
        
        self.button_save = QPushButton("Save parameters")
        self.button_save.setToolTip("Save the peak information: the parameters for the distributions of all peaks")
        self.button_save.clicked.connect(self.save_parameters)
        
        self.button_normalize = QPushButton("Normalize")
        self.button_normalize.setToolTip("Normalize the signal to sit between 0 and 1")
        self.button_normalize.clicked.connect(self.normalize)
        
        # define the text boxes
        self.textbox_title  = QLineEdit("Plot Title")
        self.textbox_xlabel = QLineEdit("X Label Name")
        self.textbox_ylabel = QLineEdit("Y Label Name")
        self.textbox_title.textChanged.connect(self.set_title)
        self.textbox_xlabel.textChanged.connect(self.set_xlabel)
        self.textbox_ylabel.textChanged.connect(self.set_ylabel)
        
        # text boxes to set the minimum and maximum
        self.textbox_min = QLineEdit("Min Value")
        self.textbox_max = QLineEdit("Max Value")
        self.textbox_min.returnPressed.connect(self.set_min_value)
        self.textbox_max.returnPressed.connect(self.set_max_value)
        self.textbox_min.setToolTip("Press Enter to Execute the Changes")
        self.textbox_max.setToolTip("Press Enter to Execute the Changes")

        
        # graphing area
        size_ratio     = 4
        self.plotter   = pg.PlotWidget()
        self.plot_item = self.plotter.getPlotItem()
        self.plotter.setBackground('w')
        
        # plotting the variables
        self.line_plots = []
        self.peak_plots = []
        
        # the layouts
        layout1 = QVBoxLayout()                     # The main layout
        layout2 = QHBoxLayout()                     # Layout for the buttons
        layout3 = QHBoxLayout()                     # Layout to store the textboxes
        layout4 = QVBoxLayout()                     # Layout for the min/max settings
        layout1.addWidget(self.plotter, size_ratio)
        layout1.addLayout(layout2)
        layout2.addWidget(self.button_load)         # add the buttons
        layout2.addWidget(self.button_run)
        layout2.addWidget(self.button_save)
        layout2.addWidget(self.button_normalize)
        # text inputs for the plots
        text_info = QLabel("Plot labels (to make changes, press the enter key after the text is edited): ")
        layout1.addWidget(text_info)
        layout3.addWidget(self.textbox_title)
        layout3.addWidget(self.textbox_xlabel)
        layout3.addWidget(self.textbox_ylabel)
        layout1.addLayout(layout3)
        # min/max to layuout 4
        layout4.addWidget(self.textbox_min)
        layout4.addWidget(self.textbox_max)
        layout3.addLayout(layout4)
        # copyright line
        dev = QLabel("For questions, e-mail the developer at: han_kyunghoon@naver.com -- © Kyunghoon Han")
        layout1.addWidget(dev)
        
        # define the main layout
        main_widget = QWidget()
        main_widget.setLayout(layout1)
        self.setCentralWidget(main_widget)
    
    def set_min_value(self):
        """sets the min x-value of the input signal
        """
        min_val = float(self.textbox_min.text())
        tmp_x_val = []
        tmp_y_val = []
        for i, x_val in enumerate(self.x_vals):
            if x_val > min_val:
                tmp_x_val.append(x_val)
                tmp_y_val.append(self.y_vals[i])
                
        self.x_vals = tmp_x_val
        self.y_vals = tmp_y_val
        self.plot_input_data()
        
        
    def set_max_value(self):
        """sets the max x-value of the input signal
        """
        max_val = float(self.textbox_max.text())
        tmp_x_val = []
        tmp_y_val = []
        for i, x_val in enumerate(self.x_vals):
            if x_val < max_val:
                print(x_val)
                tmp_x_val.append(x_val)
                tmp_y_val.append(self.y_vals[i])

        self.x_vals = tmp_x_val
        self.y_vals = tmp_y_val
        self.plot_input_data()

        
        
    
    def read_file(self):
        """
            Reads a signal file data in the following format:
                - first column  : independent variable data
                - second column : dependent variable data
        """
        dir_path     = str(abspath(os.getcwd()))
        self.file, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file to import",
            dir_path,
            'Files (*.csv, *.txt)'
        )
        
        if self.file is None:
            return None
        else:
            with open(self.file, 'r') as file:
                lines      = file.readlines()
                x_val_list = []
                y_val_list = []
                for line in lines:
                    line = line.replace(',', ' ')
                    line = line.split()
                    if len(line) > 1:
                        try:
                            x_val_list.append(float(line[0]))
                            y_val_list.append(float(line[1]))
                        except ValueError or IndexError:
                            continue
            self.x_vals = x_val_list
            self.y_vals = y_val_list
            # cache the data
            self.x_orig = self.x_vals
            self.y_orig = self.y_vals
            # plot the data for the user
            self.plot_input_data()
            # initialize the title and labels of the plot
            self.set_title()
            self.set_xlabel()
            self.set_ylabel()
            
            
    def normalize(self):
        self.y_vals = self.y_vals - np.min(self.y_vals)
        self.y_vals = self.y_vals / np.max(self.y_vals)
        self.plot_input_data()
    
    def save_parameters(self):
        if self.params is not None:
            print("the parameters being saved: ")
            print(self.params)
            options = QFileDialog.Options()
            filename, _ = QFileDialog.getSaveFileName(self,
                                "QFileDialog.getSaveFileName()","",
                                "All Files (*)", options=options)
            if filename:
                string_out = str(self.wiz_window.dist_type) + " parameters: \n"
                if self.wiz_window.dist_type == "Gaussian":
                    string_out += "Center, Amplitude, Standard_Deviation\n"
                elif self.wiz_window.dist_type == "Lorentzian":
                    string_out += "Center, Amplitude, Gamma\n"
                elif self.wiz_window.dist_type == "Voigt":
                    string_out += "Center, Amplitude, Gaussian_Width, Lorentzian_Width\n"
                else:
                    raise TypeError("The distribution name is not saved properly")
            
                with open(filename, 'w') as file:
                    file.write(string_out)
                    if self.wiz_window.dist_type == "Gaussian":
                        for param in self.params:
                            string_out = ""
                            a = param[0]
                            b = param[1] * -1.0 # somehow amplitudes are stored as negatives when they are positive
                            c = param[2]
                            string_out = str(a) + ", " + str(b) + ", " + str(c) + "\n"
                            if b > 0 :
                                file.write(string_out)
                    elif self.wiz_window.dist_type == "Lorentzian":
                        for param in self.params:
                            string_out = ""
                            a = param[0]
                            b = param[1] * -1.0 # somehow amplitudes are stored as negatives when they are positive
                            c = param[2]
                            string_out = str(a) + ", " + str(b) + ", " + str(c) + "\n"
                            if b > 0:
                                file.write(string_out)
                    elif self.wiz_window.dist_type == "Voigt":
                        for param in self.params:
                            string_out = ""
                            a = param[0]
                            b = param[1] * - 1.0 # somehow amplitudes are stored as negatives when they are positive
                            c = param[2]
                            d = param[3]
                            string_out = str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + "\n"
                            if b>0:
                                file.write(string_out)
            else:
                return None
                        
                        
            
            
    """
        Run the Wizard
    """
    def run_wizard(self):
        # re-initialize
        self.approximation  = None
        self.decompositions = []
        self.params         = []
        self.dist_type      = None
        self.plot_input_data()
        
        # recall the cached data if we want to run the method again
        x_label = self.textbox_xlabel.text()
        y_label = self.textbox_ylabel.text()
        title   = self.textbox_title.text()
        
        self.wiz_window = WizardWindow(self.x_vals, self.y_vals,  x_label=x_label, y_label=y_label, title=title)
        self.wiz_window.show()
        self.wiz_window.wizard.button(QWizard.FinishButton).clicked.connect(self.finish_wizard)
    
    def finish_wizard(self):
        if self.wiz_window.dist_type is not None:
            self.plot_input_data()
            self.plot_approx()
            self.plot_decompositions()
            self.params = self.wiz_window.params
    """
        Plotting tools
    """
    def plot_input_data(self):
        """Plot the input data called by the self.read_file function
        """
        self.plotter.clear()
        # then plot
        plot_item = self.plotter.plot(
            self.x_vals, self.y_vals, connect="finite",
            pen=pg.mkPen(width=5)
        )
        self.line_plots.append(plot_item)       # list of line plots here
        self.plotter.setContentsMargins(0, 0, 0, 0)
    
    def plot_decompositions(self):
        for dist in self.wiz_window.decompositions:
            self.plotter.plot(
                self.wiz_window.wizard.distribution.interpolation_class.x_val,
                dist,
                connect="finite",
                pen=pg.mkPen(color=(0,0,255), width=5)
            )
    
    def plot_approx(self):
        self.plotter.plot(
            self.wiz_window.wizard.distribution.interpolation_class.x_val,
            self.wiz_window.approximation,
            connect="finite",
            pen=pg.mkPen(color=(0, 255, 0), width=5)
        )
    
    def set_title(self):
        """Set the title of the plot
        """
        self.plotter.setTitle(title=self.textbox_title.text(), size='20px')
    
    def set_xlabel(self):
        """Set the x-axis label of the plot
        """
        self.plotter.setLabel('bottom', self.textbox_xlabel.text(), size='20px', color='#808080')
    
    def set_ylabel(self):
        """Set the y-axis label of the plot
        """
        self.plotter.setLabel('left', self.textbox_ylabel.text(), size='20px', color='#808080')
    8
    
        
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
