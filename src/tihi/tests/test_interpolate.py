import unittest
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from src.tihi.tihi_utils.interpolate import Interpolate  # Replace with the actual module name where Interpolate is defined

class TestInterpolate(unittest.TestCase):

    def setUp(self):
        # Setup data for testing
        self.input_x = np.linspace(0, 10, 100)
        self.input_y = np.sin(self.input_x)  # Example: sin wave
        self.interpolate_instance = Interpolate(self.input_x, self.input_y)
        
    def test_initialization(self):
        # Test if the class initializes correctly
        self.assertIsNotNone(self.interpolate_instance)
        self.assertIsNotNone(self.interpolate_instance.x_val)
        self.assertIsNotNone(self.interpolate_instance.y_val)
        self.assertEqual(len(self.interpolate_instance.x_val), 1000)  # Default domain size
        self.assertEqual(len(self.interpolate_instance.y_val), 1000)  # Default domain size

    def test_interpolation(self):
        # Test the interpolation method
        interp_x = np.linspace(0, 10, 50)
        interp_y = np.sin(interp_x)
        self.interpolate_instance.interpolate(interp_x, interp_y)
        self.assertTrue(np.allclose(self.interpolate_instance.y_val, np.sin(self.interpolate_instance.x_val), atol=1e-1))

    def test_denoise_signal(self):
        # Test the denoise signal method
        noisy_y = self.input_y + 0.1 * np.random.normal(size=self.input_y.shape)
        self.interpolate_instance.interpolate(self.input_x, noisy_y)
        self.interpolate_instance.denoise_signal()
        self.assertTrue(np.allclose(self.interpolate_instance.y_val, np.sin(self.interpolate_instance.x_val), atol=0.5))

if __name__ == '__main__':
    unittest.main()