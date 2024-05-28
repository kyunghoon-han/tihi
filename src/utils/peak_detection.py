import numpy as np

def find_peaks(class_interpolate, window_size=10, threshold=0.01):
        peaks = []

        second_deriv = second_derivative(class_interpolate)

        for i in range(window_size, len(second_deriv) - window_size):
            window_second_deriv = second_deriv[i - window_size:i + window_size + 1]
            window              = class_interpolate.y_val[i - window_size:i + window_size + 1]
            
            # Check if the central point is the maximum within its window
            if second_deriv[i] == np.min(window_second_deriv) and class_interpolate.y_val[i] > np.max(window)-threshold:
                peaks.append(i)
        
        return peaks

def second_derivative(class_interpolate):
    x_tmp = class_interpolate.x_val
    y_tmp = class_interpolate.y_val

    delta_x = x_tmp[0] - x_tmp[1]
    return np.gradient(np.gradient(y_tmp, delta_x), delta_x)
