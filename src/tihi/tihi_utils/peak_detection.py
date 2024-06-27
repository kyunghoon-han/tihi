import numpy as np

def find_peaks(class_interpolate, window_size=10, threshold=0.01, min_amp=0.0):
    """
    Find peaks in the interpolated signal based on the second derivative.

    Args:
        class_interpolate (Interpolate): Instance of Interpolate containing interpolated data.
        window_size (int, optional): Size of the window for peak detection. Defaults to 10.
        threshold (float, optional): Threshold for peak detection. Defaults to 0.01.
        min_amp (float, optional): Minimum amplitude of peaks. Defaults to 0.0.

    Returns:
        peaks (list): List of indices where peaks are detected.
    """
    peaks = []

    second_deriv = second_derivative(class_interpolate)

    for i in range(window_size, len(second_deriv) - window_size):
        window_second_deriv = second_deriv[i - window_size:i + window_size + 1]
        window              = class_interpolate.y_val[i - window_size:i + window_size + 1]
            
        bool_amplitude = class_interpolate.y_val[i] > min_amp
        bool_threshold = second_deriv[i] == np.min(window_second_deriv) and class_interpolate.y_val[i] > np.max(window)-threshold

        # Check if the central point is the maximum within its window
        # and if the amplitude is bigger than the minimum required value
        if bool_amplitude and bool_threshold:
            peaks.append(i)
        
    return peaks

def second_derivative(class_interpolate):
    """
    Compute the second derivative of the interpolated signal.

    Args:
        class_interpolate (Interpolate): Instance of Interpolate containing interpolated data.

    Returns:
        second_deriv (np.array): Array of second derivative values.
    """
    x_tmp = class_interpolate.x_val
    y_tmp = class_interpolate.y_val

    delta_x = x_tmp[0] - x_tmp[1]
    return np.gradient(np.gradient(y_tmp, delta_x), delta_x)
