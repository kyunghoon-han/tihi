import numpy as np
from scipy.interpolate import UnivariateSpline

class Interpolate():
    def __init__(self,
                 input_x,
                 input_y,
                 degree_spline=3,
                 gratings=1000):
        self.y_spline = None

        self.domain_size = int(gratings)

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
        self.y_spline = UnivariateSpline(x_in, y_in, s=0, k=self.k)
        self.x_val = np.linspace(x_in[0],
                                  x_in[-1],
                                  self.domain_size)
        self.y_val = self.y_spline(self.x_val)

        self.first_deriv = self.y_spline.derivative(n=1)(self.x_val)
        self.second_deriv = self.y_spline.derivative(n=2)(self.x_val)
        self.second_deriv = self.second_deriv/np.max(self.second_deriv)
