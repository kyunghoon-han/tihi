import sys
import unittest
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from tihi.tihi_wizardPages.baselinePage import BaselinePage, QIComboBox  # Replace with the actual module name
from tihi.tihi_utils.baseline_corrector import (linear_baseline_correction, airPLS, arPLS)


class TestBaselinePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        # Setup data for testing
        self.input_x = np.linspace(0, 10, 100)
        self.input_y = np.sin(self.input_x)  # Example: sin wave with peaks at certain intervals
        self.page = BaselinePage(self.input_x, self.input_y)

    def tearDown(self):
        self.page = None

    def test_initial_plot(self):
        # Check initial plot
        self.assertEqual(len(self.page.plotter.listDataItems()), 2)

    def test_lambda_change(self):
        # Clear and simulate changing the lambda value
        self.page.lambda_val.clear()
        QTest.keyClicks(self.page.lambda_val, '200')
        QTest.keyPress(self.page.lambda_val, Qt.Key_Enter)
        self.assertEqual(self.page.lambda_param, 200.0)


    def test_ratio_change(self):
        # Clear and simulate changing the ratio value
        self.page.ratio_val.clear()
        QTest.keyClicks(self.page.ratio_val, '1e-6')
        QTest.keyPress(self.page.ratio_val, Qt.Key_Enter)
        self.assertEqual(self.page.ratio, 1e-6)

    def test_method_change(self):
        # Simulate changing the method
        self.page.method_combobox.setCurrentIndex(1)  # Select "Linear"
        self.page.method_changes()  # Ensure method change is reflected
        self.assertEqual(self.page.method, "Linear")

    def test_run_linear(self):
        # Test running the linear baseline correction
        self.page.method_combobox.setCurrentIndex(1)  # Select "Linear"
        self.page.method_changes()  # Ensure method change is reflected
        self.page.run()
        self.assertIsNotNone(self.page.baseline)
        self.assertEqual(len(self.page.plotter.listDataItems()), 4) 

    def test_run_airPLS(self):
        # Test running the airPLS baseline correction
        self.page.method_combobox.setCurrentIndex(2)  # Select "airPLS"
        self.page.method_changes()  # Ensure method change is reflected
        self.page.run()
        self.assertIsNotNone(self.page.baseline)
        self.assertEqual(len(self.page.plotter.listDataItems()), 4)  

    def test_run_arPLS(self):
        # Test running the arPLS baseline correction
        self.page.method_combobox.setCurrentIndex(3)  # Select "arPLS"
        self.page.method_changes()  # Ensure method change is reflected
        self.page.run()
        self.assertIsNotNone(self.page.baseline)
        self.assertEqual(len(self.page.plotter.listDataItems()), 4) 

    def test_clear(self):
        # Test clearing the plot
        self.page.method_combobox.setCurrentIndex(1)  # Select "Linear"
        self.page.method_changes()  # Ensure method change is reflected
        self.page.run()
        self.page.clear()
        self.assertEqual(len(self.page.plotter.listDataItems()), 1) 

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == '__main__':
    unittest.main()
""