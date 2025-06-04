from PyQt5.QtWidgets import(
    QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout,
    QPushButton
)
from PyQt5.QtWidgets import QWizardPage, QComboBox, QSpinBox
import pyqtgraph as pg
from tihi.tihi_utils.distributions import (LorentzianFitter, GaussianFitter, VoigtFitter)
import numpy as np

class QIComboBox(QComboBox):
    '''
    Custom ComboBox class inheriting from QComboBox.
    '''
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)
        
class DistributionFittingPage(QWizardPage):
    '''
    Wizard page for fitting distributions to data.

    interpolation_class : Instance of a class containing x_val and y_val attributes for data.
    x_label             : Label for the x-axis.
    y_label             : Label for the y-axis.
    title               : Title for the plot.
    '''
    def __init__(self, interpolation_class, x_label="x-axis", y_label="y-axis", title="title"):
        super(DistributionFittingPage, self).__init__()
        
        # initialization
        self.interpolation_class = interpolation_class
        self.peak_indices        = []
        self.max_iter            = 10
        self.distribution_type   = "Gaussian"
        self.optimizer_loss      = "soft l1"
        list_distributions       = ["Gaussian", "Lorentzian", "Voigt"]
        list_optimizer_losses    = ["linear", "soft_l1", "huber", "cauchy", "arctan"]
        
        self.decompositions      = []
        self.params              = []
        self.approximation       = None
        
        # graphing tools
        self.plotter = pg.PlotWidget() # the plotting widget
        self.plotter.setBackground('w') # white background
        self.plotter.plot(interpolation_class.x_val, interpolation_class.y_val)
        self.textbox_title  = QLineEdit(title)
        self.textbox_xlabel = QLineEdit(x_label)
        self.textbox_ylabel = QLineEdit(y_label)
        
        # GUI Layouts
        self.layout1                  = QHBoxLayout()
        self.layout2                  = QVBoxLayout()
        self.layout3                  = QHBoxLayout()
        # text components
        self.label_distribution       = QLabel()
        self.label_optimizer_loss     = QLabel()
        self.label_max_iter           = QLabel()
        self.label_distribution.setText("Type of distribution to fit:")
        self.label_optimizer_loss.setText("Optimizer loss type: (default: soft_l1)")
        self.label_max_iter.setText("Maximum number of iterations (default: 50)")
        self.max_iter_spinbox         = QSpinBox()
        self.distribution_combobox    = QIComboBox()
        self.optimizer_loss_combobox  = QIComboBox()
        self.button_run               = QPushButton("Run decomposition")
        self.button_clear             = QPushButton("Clear plot")
        self.button_plot_all          = QPushButton("Plot all decompositions")
        
        # edit the components
        self.max_iter_spinbox.setMinimum(10)
        self.max_iter_spinbox.setMaximum(500)
        self.max_iter_spinbox.setValue(50)
        self.max_iter_spinbox.valueChanged.connect(self.max_iter_changes)
        for option in list_distributions:
            self.distribution_combobox.addItem(option)
        for option in list_optimizer_losses:
             self.optimizer_loss_combobox.addItem(option)
                     
        # set the layout inputs
        self.layout1.addWidget(self.plotter)
        self.layout1.addLayout(self.layout2)
        self.layout2.addWidget(self.label_distribution)
        self.layout2.addWidget(self.distribution_combobox)
        self.layout2.addWidget(self.label_optimizer_loss)
        self.layout2.addWidget(self.optimizer_loss_combobox)
        self.layout2.addWidget(self.label_max_iter)
        self.layout2.addWidget(self.max_iter_spinbox)
        
        self.layout3.addWidget(self.button_run)
        self.layout3.addWidget(self.button_clear)
        self.layout2.addLayout(self.layout3)
        self.layout2.addWidget(self.button_plot_all)
        
        self.setLayout(self.layout1)
        
        self.distribution_combobox.activated.connect(self.distribution_type_changes)
        self.optimizer_loss_combobox.activated.connect(self.method_changes)
        self.button_run.clicked.connect(self.run)
        self.button_clear.clicked.connect(self.clear)
        self.button_plot_all.clicked.connect(self.plot_all)
        
        self.plot_input_data()
    
    def distribution_type_changes(self):
        '''
        Updates the selected distribution type based on user input.
        '''
        self.distribution_type =self.distribution_combobox.currentText()
    
    def max_iter_changes(self):
        '''
        Updates the maximum iteration value based on user input.
        '''
        self.max_iter = int(self.max_iter_spinbox.value())
    
    def method_changes(self):
        '''
        Updates the optimizer loss type based on user input.
        '''
        self.optimizer_loss = str(self.optimizer_loss_combobox.currentText())
        
    def run(self):
        '''
        Executes the decomposition based on the selected distribution type.
        '''
        if self.distribution_type == "Gaussian":
            self.fitter = GaussianFitter(self.interpolation_class, self.peak_indices, max_iter=self.max_iter)
            self.params = [self.fitter.params[i:i + 3] for i in range(0, len(self.fitter.params), 3)]
            self.decompositions = [self.fitter.gaussian(self.interpolation_class.x_val, center, amp, sigma) for center, amp, sigma in self.params]
        elif self.distribution_type == "Lorentzian":
            self.fitter = LorentzianFitter(self.interpolation_class, self.peak_indices, max_iter=self.max_iter)
            self.params = [self.fitter.params[i:i + 3] for i in range(0, len(self.fitter.params), 3)]
            self.decompositions = [self.fitter.lorentzian(self.interpolation_class.x_val, centre, amp, gamma) for centre, amp, gamma in self.params]
        elif self.distribution_type == "Voigt":
            self.fitter = VoigtFitter(self.interpolation_class, self.peak_indices, self.max_iter)
            self.params = [self.fitter.params[i:i + 4] for i in range(0, len(self.fitter.params), 4)]
            self.decompositions = [self.fitter.voigt(self.interpolation_class.x_val, centre, amp, gw, lw) for centre, amp, gw, lw in self.params]
        else:
            print("Something's not working. Defaults to Gaussians.")
            self.fitter = GaussianFitter(self.interpolation_class, self.peak_indices, max_iter=self.max_iter)
            self.params = [self.fitter.params[i:i + 3] for i in range(0, len(self.fitter.params), 3)]
            self.decompositions = [self.fitter.gaussian(self.interpolation_class.x_val, center, amp, sigma) for center, amp, sigma in self.params]
        self.approximation = np.sum(self.decompositions, axis=0)
        self.plot_input_data(plot_approximation=True)
    
    def plot_all(self):
        '''
        Plots all decompositions.
        '''
        self.plot_input_data(plot_all_distributions=True)
    
    def plot_input_data(self, plot_approximation=False, plot_all_distributions=False):
        '''
        Plots the input data along with the approximation or all decompositions if specified.
        
        plot_approximation    : If True, plot the approximation. (the sum of distributions)
        plot_all_distributions: If True, plot all decompositions.
        '''
        if not plot_all_distributions:
            self.plotter.clear()
            # then plot
            self.plotter.plot(
                self.interpolation_class.x_val, self.interpolation_class.y_val, connect="finite",
                pen=pg.mkPen(width=5)
            )
            if plot_approximation:
                self.plotter.plot(
                    self.interpolation_class.x_val, self.approximation, connect="finite",
                    pen=pg.mkPen(color=(0,255,0), width=5)
                )
            
        if plot_all_distributions:
            for dist in self.decompositions:
                 self.plotter.plot(
                    self.interpolation_class.x_val, dist, connect="finite",
                    pen=pg.mkPen(color=(0,0,255), width=5)
                )
        self.plotter.setContentsMargins(0, 0, 0, 0)
    
    def clear(self):
        '''
        Clears the plot and re-plots the original data.
        '''
        self.plotter.clear()
        # Re-plot the original data after clearing
        self.plotter.plot(
            self.interpolation_class.x_val, self.interpolation_class.y_val, connect="finite",
            pen=pg.mkPen(width=5)
        )