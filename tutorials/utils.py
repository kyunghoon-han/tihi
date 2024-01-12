import numpy as np
import scipy.signal as signal
from scipy import sparse
from scipy.signal import medfilt
from scipy.sparse.linalg import spsolve
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter

def generate_fake_spectral_data(length=1000, num_peaks=10, noise_level=0.2, poly_degree=2):
    x = np.linspace(0, 10, length)
    spectral_data = np.zeros(length)

    # Generate multiple sinusoidal peaks
    for _ in range(num_peaks):
        amplitude = np.random.uniform(1, 20)  # Varying amplitude of peaks
        frequency = np.random.uniform(0.5, 10)  # Varying frequency of peaks
        phase = np.random.uniform(0, 2 * np.pi)  # Random phase shift for each peak
        peak = amplitude * np.sin(2 * np.pi * frequency * x + phase)
        spectral_data += peak

    # Add a polynomial component
    poly_coefficients = np.random.uniform(-1, 1, poly_degree + 1)  # Random coefficients for the polynomial
    polynomial = np.polyval(poly_coefficients, x)
    spectral_data += polynomial

    # Add noise to the data
    spectral_data_with_noise = spectral_data + noise_level * np.random.randn(length)

    return x, spectral_data_with_noise

def arPLS(y, ratio=1e-6, lam=100, niter=10, full_output=False):
    L = len(y)

    diag = np.ones(L - 2)
    D = sparse.spdiags([diag, -2*diag, diag], [0, -1, -2], L, L - 2)

    H = lam * D.dot(D.T)  # The transposes are flipped w.r.t the Algorithm on pg. 252

    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)

    crit = 1
    count = 0

    while crit > ratio:
        z = spsolve(W + H, W * y)
        d = y - z
        dn = d[d < 0]

        m = np.mean(dn)
        s = np.std(dn)

        w_new = 1 / (1 + np.exp(2 * (d - (2*s - m))/s))

        crit = np.linalg.norm(w_new - w) / np.linalg.norm(w)

        w = w_new
        W.setdiag(w)  # Do not create a new matrix, just update diagonal values

        count += 1

        if count > niter:
            print('Maximum number of iterations exceeded')
            break

    if full_output:
        info = {'num_iter': count, 'stop_criterion': crit}
        return z, d, info
    else:
        return z

class Interpolate():
    def __init__(self,
                 input_x,
                 input_y,
                 degree_spline=3,
                 gratings=1000,
                 denoising_window_size=30,
                 denoising_order=3):
        """_summary_

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
        self.y_spline = UnivariateSpline(x_in, y_in, s=0, k=self.k)
        self.x_val = np.linspace(x_in[0],
                                  x_in[-1],
                                  self.domain_size)
        self.y_val = self.y_spline(self.x_val)

        self.first_deriv = self.y_spline.derivative(n=1)(self.x_val)
        self.second_deriv = self.y_spline.derivative(n=2)(self.x_val)
        self.second_deriv = self.second_deriv/np.max(self.second_deriv)
        
    def denoise_signal(self):
        denoised_y = savgol_filter(self.y_val, window_length=self.denoising_window, polyorder=self.denoising_order)
        self.interpolate(self.x_val, denoised_y)
        
def find_peaks(class_interpolate, window_size=10, threshold=0.01):
        peaks = []
                
        for i in range(window_size, len(class_interpolate.second_deriv) - window_size):
            window_second_deriv = class_interpolate.second_deriv[i - window_size:i + window_size + 1]
            window              = class_interpolate.y_val[i - window_size:i + window_size + 1]
            
            # Check if the central point is the maximum within its window
            if class_interpolate.second_deriv[i] == np.min(window_second_deriv) and class_interpolate.y_val[i] > np.max(window)-threshold:
                peaks.append(i)
        
        return peaks