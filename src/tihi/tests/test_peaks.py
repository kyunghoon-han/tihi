import unittest
import numpy as np
from src.tihi.tihi_utils.peak_detection import find_peaks, second_derivative  # Replace with the actual module name
from src.tihi.tihi_utils.interpolate import Interpolate

class TestPeakFinding(unittest.TestCase):

    def setUp(self):
        # Setup data for testing
        self.input_x = np.linspace(0, 10, 1000)
        self.input_y = np.sin(self.input_x)  # Example: sin wave with peaks at certain intervals
        self.interpolate_instance = Interpolate(self.input_x, self.input_y, gratings=1000)

    def test_second_derivative(self):
        # Test the second_derivative function
        second_deriv = second_derivative(self.interpolate_instance)
        expected_second_deriv = -np.sin(self.input_x)  # Second derivative of sin(x) is -sin(x)
        self.assertTrue(np.allclose(second_deriv, expected_second_deriv, atol=0.3))

    def test_find_peaks(self):
        # Test the find_peaks function
        peaks = find_peaks(self.interpolate_instance, window_size=5, threshold=0.5, min_amp=0.5)
        # The peaks of sin(x) in the range [0, 10] are at x = pi/2, 5pi/2
        expected_peaks_x = np.array([np.pi/2, 5*np.pi/2])
        expected_peaks_indices = [np.argmin(np.abs(self.input_x - peak_x)) for peak_x in expected_peaks_x]
        self.assertEqual(peaks, expected_peaks_indices)

if __name__ == '__main__':
    unittest.main()