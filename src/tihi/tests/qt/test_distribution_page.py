import sys
import unittest
import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from tihi.tihi_utils.distributions import LorentzianFitter, GaussianFitter, VoigtFitter
from tihi.tihi_utils.interpolate import Interpolate
from tihi.tihi_wizardPages.distributionPage import DistributionFittingPage, QIComboBox  


class TestDistributionFittingPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        x_val = np.linspace(0, 10, 100)
        y_val = np.sin(x_val)  # Example data
        
        self.interpolation_class = Interpolate(x_val, y_val, gratings=100)
        self.page = DistributionFittingPage(self.interpolation_class)
        self.page.interpolation_class = self.interpolation_class
        
        expected_peaks_x = np.array([np.pi/2, 5*np.pi/2])
        self.input_x = x_val
        self.page.peak_indices = [np.argmin(np.abs(self.input_x - peak_x)) for peak_x in expected_peaks_x]

    def tearDown(self):
        self.page = None

    def test_initial_plot(self):
        # Check initial plot
        self.assertEqual(len(self.page.plotter.listDataItems()), 1)

    def test_distribution_type_change(self):
        # Simulate changing the distribution type
        self.page.distribution_combobox.setCurrentIndex(1)  # Select "Lorentzian"
        self.page.distribution_type_changes()  # Ensure method change is reflected
        self.assertEqual(self.page.distribution_type, "Lorentzian")

    def test_optimizer_loss_change(self):
        # Simulate changing the optimizer loss type
        self.page.optimizer_loss_combobox.setCurrentIndex(2)  # Select "huber"
        self.page.method_changes()  # Ensure method change is reflected
        self.assertEqual(self.page.optimizer_loss, "huber")

    def test_max_iter_change(self):
        # Simulate changing the max iterations
        self.page.max_iter_spinbox.setValue(10)
        self.assertEqual(self.page.max_iter_spinbox.value(), 10)

    def test_run_gaussian(self):
        # Test running the Gaussian fitter
        self.page.distribution_combobox.setCurrentIndex(0)  # Select "Gaussian"
        self.page.distribution_type_changes()
        self.page.run()
        self.assertIsNotNone(self.page.approximation)
        self.assertEqual(len(self.page.plotter.listDataItems()), 2)  # original and approximation

    def test_run_lorentzian(self):
        # Test running the Lorentzian fitter
        self.page.distribution_combobox.setCurrentIndex(1)  # Select "Lorentzian"
        self.page.distribution_type_changes()
        self.page.run()
        self.assertIsNotNone(self.page.approximation)
        self.assertEqual(len(self.page.plotter.listDataItems()), 2)  # original and approximation

    def test_run_voigt(self):
        # Test running the Voigt fitter
        self.page.distribution_combobox.setCurrentIndex(2)  # Select "Voigt"
        self.page.distribution_type_changes()
        self.page.run()
        self.assertIsNotNone(self.page.approximation)
        self.assertEqual(len(self.page.plotter.listDataItems()), 2)  # original and approximation

    def test_plot_all_decompositions(self):
        # Test plotting all decompositions
        self.page.distribution_combobox.setCurrentIndex(0)  # Select "Gaussian"
        self.page.distribution_type_changes()
        self.page.run()
        self.page.plot_all()
        self.assertGreater(len(self.page.plotter.listDataItems()), 3)  # original, approximation, decompositions

    def test_clear_plot(self):
        # Test clearing the plot
        self.page.run()
        print("Before clear:", len(self.page.plotter.listDataItems()))
        self.page.clear()
        print("After clear:", len(self.page.plotter.listDataItems()))
        self.assertEqual(len(self.page.plotter.listDataItems()), 1) # I am keeping the original input data

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

if __name__ == '__main__':
    unittest.main()
""