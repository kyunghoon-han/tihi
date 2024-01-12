from scipy.optimize import least_squares
from scipy.special import wofz
import numpy as np

class GaussianFitter():
    def __init__(self, InterpolatedData, peaks,
                 max_iter=100):
        self.x_vals = InterpolatedData.x_val
        self.y_vals = InterpolatedData.y_val
        
        # initial parameters
        self.centers = self.x_vals[peaks]
        self.amplitudes = self.y_vals[peaks]
        self.sigmas = np.random.rand(*self.amplitudes.shape)
        self.params = np.array([self.centers, self.amplitudes,self.sigmas]).T  
        self.start_params = self.params.flatten().tolist()
        self.decompositions = []
        # result to output
        self.result = None
                
        self.approximator(max_iter)
        
    def approximator(self, max_iter):
        self.params = least_squares(self.residual,
                            self.start_params, args=(self.x_vals, self.y_vals),
                            bounds=(-np.max(self.x_vals),
                                    np.max(self.x_vals)),
                            ftol=1e-9, xtol=1e-9, loss='soft_l1',
                            f_scale=0.1, max_nfev=max_iter).x
        print(self.params)
        print("the error for this run is: ", np.mean(self.residual(self.params, self.x_vals, self.y_vals)))

        self.results = np.array([self.gaussian_sum(x, self.params) for x in self.x_vals])
        error = np.mean(np.abs(self.y_vals - self.results))
        
        return error
    
    def gaussian(self, x, center, amplitude, sigma):
        amplitude = amplitude * (-1.0)
        return amplitude * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))

    def gaussian_sum(self, x, params):
        params = params.flatten().tolist()
        params = [params[i:i + 3] for i in range(0, len(params), 3)]
        self.decompositions = [self.gaussian(x, center, amp, sigma) for center, amp, sigma in params]
        return np.sum(self.decompositions, axis=0)

    def residual(self, params, x_vals, y_vals):
        return y_vals - self.gaussian_sum(x_vals, params)

class LorentzianFitter():
    def __init__(self, InterpolatedData, peaks,
                 max_iter=100):
        self.x_vals = InterpolatedData.x_val
        self.y_vals = InterpolatedData.y_val
        
        # initial parameters
        self.centers = self.x_vals[peaks]
        self.amplitudes = self.y_vals[peaks]
        self.gammas = [1]*len(self.centers)
        self.params = np.array([self.centers, self.amplitudes,self.gammas]).T
        self.start_params = self.params.flatten().tolist()
        self.decompositions = []

        self.approximator(max_iter)
        
    def approximator(self, max_iter):
        self.params = least_squares(self.residual,
                            self.start_params, args=(self.x_vals, self.y_vals),
                            bounds=(-np.max(self.x_vals),
                                    np.max(self.x_vals)),
                            ftol=1e-9, xtol=1e-9, loss='soft_l1',
                            f_scale=0.1, max_nfev=max_iter).x
        print(self.params)
        print("the error for this run is: ", np.mean(self.residual(self.params, self.x_vals, self.y_vals)))

        self.results = np.array([self.lorentzian_sum(x, self.params) for x in self.x_vals])
        error = np.mean(np.abs(self.y_vals - self.results))
        
        return error
    
    def lorentzian(self, x, center, amplitude, gamma):
        amplitude = amplitude * (-1.0)
        return amplitude * (gamma / np.pi) / ((x - center) ** 2 + gamma ** 2)

    def lorentzian_sum(self, x, params):
        params = params.tolist()
        params = [params[i:i + 3] for i in range(0, len(params), 3)]
        self.decompositions = [self.lorentzian(x, centre, amp, gamma) for centre, amp, gamma in params]
        return np.sum(self.decompositions, axis=0)

    def residual(self, params, x_vals, y_vals):
        return y_vals - self.lorentzian_sum(x_vals, params)
    
class VoigtFitter():
    def __init__(self, InterpolatedData, peaks, max_iter=50):
        self.x_vals = InterpolatedData.x_val
        self.y_vals = InterpolatedData.y_val
        
        # initial parameters
        self.centers = self.x_vals[peaks]
        self.amplitudes = self.y_vals[peaks]
        self.gauss_widths = np.ones_like(self.amplitudes) #np.random.rand(*self.amplitudes.shape)
        self.lorentz_widths = np.ones_like(self.amplitudes) #np.random.rand(*self.amplitudes.shape)
        self.params = np.array([self.centers, self.amplitudes, self.gauss_widths, self.lorentz_widths]).T
        self.start_params = self.params.flatten().tolist()
        num_dists = len(self.centers)
        self.decompositions = []
        
        self.approximator(max_iter)
        
    def approximator(self, max_iter):
        self.params = least_squares(self.residual,
                            self.start_params, args=(self.x_vals, self.y_vals),
                            bounds=(-np.max(self.x_vals), np.max(self.x_vals)),
                            ftol=1e-9, xtol=1e-9, loss='soft_l1',
                            f_scale=0.1, max_nfev=max_iter).x
        print(self.params)
        print("the error for this run is: ", np.mean(self.residual(self.params, self.x_vals, self.y_vals)))

        self.results = np.array([self.voigt_sum(x, self.params) for x in self.x_vals])
        error = np.mean(np.abs(self.y_vals - self.results))
        
        return error
    
    def voigt(self, x, center, amplitude, gauss_width, lorentz_width):
        sigma = gauss_width / np.sqrt(2 * np.log(2))
        gamma = lorentz_width
        z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2) + 1e-20)
        return amplitude * np.real(wofz(z)).astype(float) / (sigma * np.sqrt(2 * np.pi) + 1e-20)

    def voigt_sum(self, x, params):
        params = params.tolist()
        params = [params[i:i + 4] for i in range(0, len(params), 4)]
        self.decompositions = [self.voigt(x, centre, amp, gw, lw) for centre, amp, gw, lw in params]
        return np.sum(self.decompositions, axis=0)

    def residual(self, params, x_vals, y_vals):
        return y_vals - self.voigt_sum(x_vals, params)