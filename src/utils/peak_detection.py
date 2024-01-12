import numpy as np

def find_peaks(class_interpolate, window_size=10, threshold=0.01):
        peaks = []
                
        for i in range(window_size, len(class_interpolate.second_deriv) - window_size):
            window_second_deriv = class_interpolate.second_deriv[i - window_size:i + window_size + 1]
            window              = class_interpolate.y_val[i - window_size:i + window_size + 1]
            
            # Check if the central point is the maximum within its window
            if class_interpolate.second_deriv[i] == np.min(window_second_deriv) and class_interpolate.y_val[i] > np.max(window)-threshold:
                peaks.append(i)
        
        return peaks