#!/usr/bin/env python

from PyQt5.QtWidgets import QWizard
from wizardPages.interpolatePage import InterpolationPage as ipp
from wizardPages.baselinePage import BaselinePage as blp
from wizardPages.peak_detectionPage import PeakDetectionPage as pdp
from wizardPages.distributionPage import DistributionFittingPage as dfp

from utils.interpolate import Interpolate
import numpy as np

class MagicWizard(QWizard):
    def __init__(self, x_vals, y_vals, x_label="x-axis", y_label="y-axis", title="title"):
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
        # Disable the "go back" button on the first page
        backButton = self.button(QWizard.BackButton)
        if backButton:
            backButton.hide()
        
    def finish_line(self):
        return None
    
    def next_button(self):
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
        return None
    
    def initializePage(self, pageId):
        super().initializePage(pageId)

        # Disable the "go back" button on the first page
        if pageId == self.pageIds()[0]:
            self.button(QWizard.BackButton).setDisabled(True)