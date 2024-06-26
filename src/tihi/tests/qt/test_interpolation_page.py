import unittest
from PyQt5.QtWidgets import QApplication
from tihi.tihi_utils.interpolate import Interpolate
from unittest.mock import MagicMock, patch
from tihi.tihi_wizardPages.interpolatePage import InterpolationPage
import numpy as np
import sys

# This is required to create a QApplication instance, as it is needed to test Qt widgets
app = QApplication(sys.argv)

class TestInterpolationPage(unittest.TestCase):
    
    def setUp(self):
        # Create some dummy data for testing
        self.x_vals = np.linspace(0, 10, 1000)
        self.y_vals = np.sin(self.x_vals)
        # Add noise to the y-values
        noise = np.random.normal(0, 0.6, self.y_vals.shape)  # Adjust noise level as needed
        self.y_vals_noisy = self.y_vals + noise
        
        self.page = InterpolationPage(self.x_vals, self.y_vals)
    
    def test_initialization(self):
        self.assertEqual(self.page.x_orig.tolist(), self.x_vals.tolist())
        self.assertEqual(self.page.y_orig.tolist(), self.y_vals.tolist())
        self.assertEqual(self.page.num_points, len(self.x_vals))
        self.assertEqual(self.page.textbox_title.text(), "title")
        self.assertEqual(self.page.textbox_xlabel.text(), "x-axis")
        self.assertEqual(self.page.textbox_ylabel.text(), "y-axis")
    
    def test_plot_input_data(self):
        self.page.plot_input_data() # somehow I am plotting this three times
        self.assertEqual(len(self.page.plotter.listDataItems()), 3)
    
    def test_clear(self):
        self.page.clear()
        self.assertEqual(self.page.num_points, len(self.x_vals))
        self.assertEqual(len(self.page.plotter.listDataItems()), 1)
        self.assertEqual(self.page.x_vals.tolist(), self.x_vals.tolist())
        self.assertEqual(self.page.y_vals.tolist(), self.y_vals.tolist())
    
    def test_change_numpoints(self):
        self.page.text_numpoints.setText("50")
        self.assertEqual(self.page.num_points, 50)
    
    def test_change_denoise_window_size(self):
        self.page.text_denoise_window_size.setText("20")
        self.assertEqual(self.page.denoise_window, 20)
    
    def test_interpolate_data(self):
        mock_interpolated = Interpolate(self.x_vals, self.y_vals, gratings=100)
        mock_interpolated.x_val = self.x_vals
        mock_interpolated.y_val = self.y_vals
        
        self.page.interpolate_data()
        
        self.assertEqual(self.page.x_vals.tolist(), self.x_vals.tolist())
        self.assertEqual(self.page.y_vals.tolist(), self.y_vals.tolist())
        self.assertEqual(len(self.page.plotter.listDataItems()), 3)


if __name__ == '__main__':
    unittest.main()