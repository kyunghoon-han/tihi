import unittest
import numpy as np
from scipy.optimize import least_squares
from scipy.special import wofz
from tihi.tihi_utils.distributions import GaussianFitter, LorentzianFitter, VoigtFitter
from tihi.tihi_utils.interpolate import Interpolate

class TestGaussianFitter(unittest.TestCase):
    
    def setUp(self):
        # Setup data for testing
        self.x_vals = np.linspace(0, 10, 10)
        self.y_vals = np.exp(-(self.x_vals - 5)**2 / 2)  # Gaussian peak centered at 5
        self.interpolated = Interpolate(self.x_vals, self.y_vals,gratings=10)
        
    def test_gaussian_fitter(self):
        # Test case for GaussianFitter
        peaks = [50]  # Index of the peak (approximately centered at x = 5)
        fitter = GaussianFitter(self.interpolated, peaks, max_iter=500)
        self.assertTrue(np.allclose(fitter.results, self.y_vals, atol=1e-2))  # Check if fitted Gaussian matches original
        
    # Add more test cases as needed

class TestLorentzianFitter(unittest.TestCase):
    
    def setUp(self):
        # Setup data for testing
        self.x_vals = np.linspace(0, 10, 100)
        self.y_vals = 1 / ((self.x_vals - 5)**2 + 1)  # Lorentzian peak centered at 5
        self.interpolated = Interpolate(self.x_vals, self.y_vals, gratings=100)
        
    def test_lorentzian_fitter(self):
        # Test case for LorentzianFitter
        peaks = [50]  # Index of the peak (approximately centered at x = 5)
        fitter = LorentzianFitter(self.interpolated, peaks)
        self.assertTrue(np.allclose(fitter.results, self.y_vals, atol=1e-2))  # Check if fitted Lorentzian matches original
        
    # Add more test cases as needed

class TestVoigtFitter(unittest.TestCase):
    
    def setUp(self):
        # Setup data for testing
        self.x_vals = np.linspace(0, 10, 100)
        self.y_vals = np.real(wofz((self.x_vals - 5) + 1j)) / (np.sqrt(2 * np.pi))  # Voigt peak centered at 5
        self.interpolated = Interpolate(self.x_vals, self.y_vals, gratings=100)
        
    def test_voigt_fitter(self):
        # Test case for VoigtFitter
        peaks = [50]  # Index of the peak (approximately centered at x = 5)
        fitter = VoigtFitter(self.interpolated, peaks)
        self.assertTrue(np.allclose(fitter.results, self.y_vals, atol=1e-2))  # Check if fitted Voigt matches original
        
    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()

