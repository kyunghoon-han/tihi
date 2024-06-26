import unittest
from PyQt5.QtWidgets import QApplication
from unittest.mock import MagicMock, patch
from tihi.tihi_wizardPages.peak_detectionPage import PeakDetectionPage
import numpy as np
import sys

# This is required to create a QApplication instance, as it is needed to test Qt widgets
app = QApplication(sys.argv)

class TestPeakDetectionPage(unittest.TestCase):
    
    def setUp(self):
        # Create a mock Interpolate class instance with dummy data for testing
        self.mock_interpolation = MagicMock()
        self.mock_interpolation.x_val = np.linspace(0, 10, 100)
        self.mock_interpolation.y_val = np.sin(self.mock_interpolation.x_val)
        self.page = PeakDetectionPage(self.mock_interpolation)
    
    def test_initialization(self):
        self.assertEqual(self.page.interpolation_class, self.mock_interpolation)
        self.assertEqual(self.page.window_size, 10)
        self.assertEqual(self.page.threshold, 0.1)
        self.assertEqual(self.page.min_amps, 0.0)
        self.assertEqual(self.page.textbox_title.text(), "title")
        self.assertEqual(self.page.textbox_xlabel.text(), "x-axis")
        self.assertEqual(self.page.textbox_ylabel.text(), "y-axis")
    
    def test_plot_input_data(self):
        self.page.plot_input_data()
        self.assertEqual(len(self.page.plotter.listDataItems()), 1)
    
    def test_clear(self):
        self.page.clear()
        self.assertEqual(len(self.page.plotter.listDataItems()), 0)
    
    def test_window_size_changes(self):
        self.page.window_size_edit.setText("20")
        self.assertEqual(self.page.window_size, 20)
    
    def test_threshold_changes(self):
        self.page.threshold_edit.setText("0.2")
        self.assertEqual(self.page.threshold, 0.2)
    
    def test_min_amp_changes(self):
        self.page.min_amp_edit.setText("0.5")
        self.assertEqual(self.page.min_amps, 0.5)
    
    @patch('tihi.tihi_utils.peak_detection.find_peaks')
    def test_run(self, mock_find_peaks):
        mock_find_peaks.return_value = [10, 20, 30]
        self.page.run()
        
        mock_find_peaks.assert_called_once_with(
            self.mock_interpolation,
            window_size=self.page.window_size,
            threshold=self.page.threshold,
            min_amp=self.page.min_amps
        )
        self.assertEqual(self.page.peak_indices, [10, 20, 30])
        self.assertEqual(len(self.page.plotter.listDataItems()), 2)

if __name__ == '__main__':
    unittest.main()
