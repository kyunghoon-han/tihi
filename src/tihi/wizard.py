#!/usr/bin/env python

from PyQt5.QtWidgets import QWizard
from tihi.tihi_wizardPages.interpolatePage import InterpolationPage as ipp
from tihi.tihi_wizardPages.baselinePage import BaselinePage as blp
from tihi.tihi_wizardPages.peak_detectionPage import PeakDetectionPage as pdp
from tihi.tihi_wizardPages.distributionPage import DistributionFittingPage as dfp

from tihi.tihi_utils.interpolate import Interpolate
import numpy as np

class MagicWizard(QWizard):
    """
    Wizard for peak profiling using PyQt5 and custom pages.

    Attributes:
        out_profiles (list): List to store output profiles.
        out_params (list): List to store output parameters.
        out_model: Placeholder for output model.
        page_num (int): Current page number.
        interpolate (ipp): Interpolation page instance.
        baseline (blp): Baseline fitting page instance.
        peak_detect (pdp): Peak detection page instance.
        distribution (dfp): Distribution fitting page instance.
    """
    def __init__(self, x_vals, y_vals, x_label="x-axis", y_label="y-axis", title="title"):
        """
        Initialize the MagicWizard instance.

        Args:
            x_vals (np.ndarray): Array of x-axis values.
            y_vals (np.ndarray): Array of y-axis values.
            x_label (str, optional): Label for the x-axis. Defaults to "x-axis".
            y_label (str, optional): Label for the y-axis. Defaults to "y-axis".
            title (str, optional): Title of the wizard. Defaults to "title".
        """
        super(MagicWizard, self).__init__()
        # Set the initial size of the wizard window
        self.setGeometry(100, 100, 800, 600)  # Adjust the values as needed
        # Disable the back button on initialization
        self.button(QWizard.BackButton).hide()
        # initial Interpolate class definition
        initial_interpolation = Interpolate(
                x_vals, y_vals,
                gratings = 100,
                denoising_window_size = 10)
        # the outputs
        self.out_profiles = []
        self.out_params   = []
        self.out_model    = None
        self.page_num     = 1
        # pages
        self.interpolate  = ipp(x_vals, y_vals,
                                x_label=x_label,
                                y_label=y_label,
                                title=title)
        self.baseline     = blp(self.interpolate.x_vals,
                                self.interpolate.y_vals,
                                x_label=x_label,
                                y_label=y_label,
                                title=title)
        self.peak_detect  = pdp(initial_interpolation,
                                x_label=x_label,
                                y_label=y_label,
                                title=title)
        self.distribution = dfp(initial_interpolation,
                                x_label=x_label,
                                y_label=y_label,
                                title=title)
        
        # add the pages
        self.addPage(self.interpolate)
        self.addPage(self.baseline)
        self.addPage(self.peak_detect)
        self.addPage(self.distribution)
        # title & size of the wizard window
        self.setWindowTitle("Peak profiler wizard")
        #self.resize(640,480)
        self.button(QWizard.NextButton).clicked.connect(self.next_button)
        self.button(QWizard.BackButton).clicked.connect(self.back_button)
        self.button(QWizard.FinishButton).clicked.connect(self.finish_line)
        
        self.currentIdChanged.connect(self.handlePageChange)
        self.handlePageChange()

    def handlePageChange(self):
        """
        Handle changes in wizard pages.

        Disables the "go back" button on the first page.
        """
        backButton = self.button(QWizard.BackButton)
        if backButton:
            backButton.hide()
        
    def finish_line(self):
        """
        Placeholder method for finishing the wizard.

        Returns:
            None
        """
        return None
    
    def next_button(self):
        """
        Move to the next wizard page based on the current page number.

        Returns:
            None
        """
        self.page_num += 1
        if self.page_num == 2:
            self.baseline.x_vals = self.interpolate.x_vals
            self.baseline.y_vals = self.interpolate.y_vals
            self.baseline.clear()
            self.baseline.plot_input_data()
        elif self.page_num == 3:
            intermediate_result = Interpolate(
                self.baseline.x_vals, self.baseline.y_vals,
                gratings = self.interpolate.num_points,
                denoising_window_size = int(self.interpolate.text_denoise_window_size.text()))
            self.peak_detect.interpolation_class = intermediate_result
            self.peak_detect.plot_input_data()
        elif self.page_num==4:
            self.distribution.interpolation_class = self.peak_detect.interpolation_class
            self.distribution.peak_indices        = self.peak_detect.peak_indices
            self.distribution.plot_input_data()
        return None
    
    def back_button(self):
        """
        Placeholder method for handling the back button.

        Returns:
            None
        """
        return None
    
    def initializePage(self, pageId):
        """
        Initialize wizard pages and manage the "go back" button's visibility.

        Args:
            pageId: ID of the wizard page being initialized.

        Returns:
            None
        """
        super().initializePage(pageId)

        # Disable the "go back" button on the first page
        if pageId == self.pageIds()[0]:
            self.button(QWizard.BackButton).setDisabled(True)