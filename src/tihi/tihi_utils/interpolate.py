import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter


class Interpolate():
    def __init__(self,
                 input_x,
                 input_y,
                 degree_spline=3,
                 gratings=1000,
                 denoising_window_size=30,
                 denoising_order=3):
        """Signal interpolation and denoising algorithm

        Args:
            input_x (1D np array): array of the x-variables
            input_y (1D np array): array of the y-variables
            degree_spline (int, optional): degree of spline interpolation. Defaults to 3.
            gratings (int, optional): number of datapoints obtained by the interpolation. Defaults to 1000.
            denoising_window_size (int, optional) : size of the window used to denoise the interpolated signal. Defaults to 30
            denoising_order (int, optional) : order of the polynomial for the Savitzky-Golay filter.Defaults to 3
        """
        self.y_spline = None

        self.domain_size = int(gratings)
        self.denoising_window = denoising_window_size
        self.denoising_order  = denoising_order

        self.x_val = None
        self.y_val = None

        # degree of the smoothing spline
        self.k = degree_spline
        if self.k > 5:
            self.k = 5
        elif self.k < 1:
            self.k = 1

        self.first_deriv = None
        self.second_deriv = None

        if np.max(input_y) > 1:
            input_y = input_y / np.max(input_y)

        self.interpolate(input_x, input_y)

    def interpolate(self, x_in, y_in):
        self.y_spline = interp1d(x_in, y_in) #  s=0, k=self.k)
        self.x_val = np.linspace(x_in[0],
                                  x_in[-1],
                                  self.domain_size)
        self.y_val = self.y_spline(self.x_val)

        #self.first_deriv = self.y_spline.derivative(n=1)(self.x_val)
        #self.second_deriv = self.y_spline.derivative(n=2)(self.x_val)
        #self.second_deriv = self.second_deriv/np.max(self.second_deriv)
        
    def denoise_signal(self):
        denoised_y = savgol_filter(self.y_val, window_length=self.denoising_window, polyorder=self.denoising_order)
        self.interpolate(self.x_val, denoised_y)
