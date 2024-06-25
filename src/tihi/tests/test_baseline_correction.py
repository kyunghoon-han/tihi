import unittest
import numpy as np
from scipy import sparse
from scipy.signal import medfilt
from scipy.sparse.linalg import spsolve
from src.tihi.tihi_utils.interpolate import Interpolate
from src.tihi.tihi_utils.baseline_corrector import linear_baseline_correction, airPLS, arPLS

class TestBaselineCorrection(unittest.TestCase):
    
    def test_linear_baseline_correction(self):
        # Test case 1: Basic test with linear data
        x_val = np.arange(100)
        y_val = np.linspace(0, 10, 100)  # Linear data
        corrected_baseline = linear_baseline_correction(x_val, y_val)
        self.assertEqual(corrected_baseline.shape, (100,))
        
        # Test case 2: Test with random data
        np.random.seed(0)
        y_val = np.random.normal(size=100)
        corrected_baseline = linear_baseline_correction(x_val, y_val)
        self.assertEqual(corrected_baseline.shape, (100,))
    
    def test_airPLS(self):
        # Test case for airPLS
        y = np.random.normal(size=100)
        baseline = airPLS(y)
        self.assertEqual(baseline.shape, (100,))
    
    def test_arPLS(self):
        # Test case for arPLS
        y = np.random.normal(size=100)
        baseline = arPLS(y)
        self.assertEqual(baseline.shape, (100,))
    
    def test_exceptions(self):
        # Test case for linear_baseline_correction exception handling
        x_val = np.arange(10)
        y_val = np.random.normal(size=10)
        with self.assertRaises(ValueError):
            linear_baseline_correction(x_val, y_val, percentile=99)  # Adjust percentile to trigger exception

if __name__ == '__main__':
    unittest.main()