from scipy.optimize import least_squares
from scipy.special import wofz
import numpy as np

class GaussianFitter():
    def __init__(self, InterpolatedData, peaks,
                 max_iter=100):
        '''
        Gaussian peak fitting class.

        Parameters:
        InterpolatedData : object
                           Interpolated data object containing x_val and y_val.
        peaks            : array_like
                           Indices of peaks in the data.
        max_iter         : int, optional (default=100)
                           Maximum number of iterations for fitting.

        Attributes:
        x_vals           : ndarray
                           X values from InterpolatedData.
        y_vals           : ndarray
                           Y values from InterpolatedData.
        centers          : ndarray
                           Initial centers of Gaussian peaks.
        amplitudes       : ndarray
                           Initial amplitudes of Gaussian peaks.
        sigmas           : ndarray
                           Initial standard deviations of Gaussian peaks.
        params           : ndarray
                           Array of initial parameters for least squares fitting.
        start_params     : list
                           Flattened list of initial parameters.
        decompositions   : list
                           List to store individual Gaussian functions.
        result           : None
                           Placeholder for fitting result.
        '''
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
        '''
        Perform Gaussian fitting using least squares optimization.

        Parameters:
        max_iter : int
                   Maximum number of iterations for fitting.

        Returns:
        error    : float
                   Mean absolute error of the fitting.

        Notes:
        Uses soft L1 loss and bounds parameters to constrain optimization.
        '''
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
        '''
        Calculate a Gaussian function.

        Parameters:
        x         : ndarray
                    X values.
        center    : float
                    Center of the Gaussian function.
        amplitude : float
                    Amplitude of the Gaussian function.
        sigma     : float
                    Standard deviation of the Gaussian function.

        Returns:
        ndarray
        '''
        amplitude = amplitude * (-1.0)
        return amplitude * np.exp(-(x - center) ** 2 / (2 * sigma ** 2))

    def gaussian_sum(self, x, params):
        '''
        Calculate the sum of Gaussian functions.

        Parameters:
        x      : ndarray
                 X values.
        params : ndarray
                 Array of parameters for Gaussian functions.

        Returns:
        ndarray
        '''
        params = params.flatten().tolist()
        params = [params[i:i + 3] for i in range(0, len(params), 3)]
        self.decompositions = [self.gaussian(x, center, amp, sigma) for center, amp, sigma in params]
        return np.sum(self.decompositions, axis=0)

    def residual(self, params, x_vals, y_vals):
        '''
        Calculate residual between data and Gaussian fit.

        Parameters:
        params : ndarray
                 Array of parameters for Gaussian functions.
        x_vals : ndarray
                 X values of the data.
        y_vals : ndarray
                 Y values of the data.

        Returns:
        ndarray
        '''
        return y_vals - self.gaussian_sum(x_vals, params)

class LorentzianFitter():
    '''
        Lorentzian peak fitting class.

        Parameters:
        InterpolatedData : object
                           Interpolated data object containing x_val and y_val.
        peaks            : array_like
                           Indices of peaks in the data.
        max_iter         : int, optional (default=100)
                           Maximum number of iterations for fitting.

        Attributes:
        x_vals           : ndarray
                           X values from InterpolatedData.
        y_vals           : ndarray
                           Y values from InterpolatedData.
        centers          : ndarray
                           Initial centers of Lorentzian peaks.
        amplitudes       : ndarray
                           Initial amplitudes of Lorentzian peaks.
        gammas           : list
                           Initial full width at half maximum (FWHM) of Lorentzian peaks.
        params           : ndarray
                           Array of initial parameters for least squares fitting.
        start_params     : list
                           Flattened list of initial parameters.
        decompositions   : list
                           List to store individual Lorentzian functions.
        '''
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
        '''
        Perform Lorentzian fitting using least squares optimization.

        Parameters:
        max_iter : int
                   Maximum number of iterations for fitting.

        Returns:
        error    : float
                   Mean absolute error of the fitting.

        Notes:
        Uses soft L1 loss and bounds parameters to constrain optimization.
        '''
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
        '''
        Calculate a Lorentzian function.

        Parameters:
        x         : ndarray
                    X values.
        center    : float
                    Center of the Lorentzian function.
        amplitude : float
                    Amplitude of the Lorentzian function.
        gamma     : float
                    Full width at half maximum (FWHM) of the Lorentzian function.

        Returns:
        ndarray
        '''
        amplitude = amplitude * (-1.0)
        return amplitude * (gamma / np.pi) / ((x - center) ** 2 + gamma ** 2)

    def lorentzian_sum(self, x, params):
        '''
        Calculate the sum of Lorentzian functions.

        Parameters:
        x      : ndarray
                 X values.
        params : ndarray
                 Array of parameters for Lorentzian functions.

        Returns:
        ndarray
        '''
        params = params.tolist()
        params = [params[i:i + 3] for i in range(0, len(params), 3)]
        self.decompositions = [self.lorentzian(x, centre, amp, gamma) for centre, amp, gamma in params]
        return np.sum(self.decompositions, axis=0)

    def residual(self, params, x_vals, y_vals):
        '''
        Calculate residual between data and Lorentzian fit.

        Parameters:
        params : ndarray
                 Array of parameters for Lorentzian functions.
        x_vals : ndarray
                 X values of the data.
        y_vals : ndarray
                 Y values of the data.

        Returns:
        ndarray
        '''
        return y_vals - self.lorentzian_sum(x_vals, params)
    
class VoigtFitter():
    def __init__(self, InterpolatedData, peaks, max_iter=50):
        '''
        Voigt peak fitting class.

        Parameters:
        InterpolatedData : object
                           Interpolated data object containing x_val and y_val.
        peaks            : array_like
                           Indices of peaks in the data.
        max_iter         : int, optional (default=50)
                           Maximum number of iterations for fitting.

        Attributes:
        x_vals           : ndarray
                           X values from InterpolatedData.
        y_vals           : ndarray
                           Y values from InterpolatedData.
        centers          : ndarray
                           Initial centers of Voigt peaks.
        amplitudes       : ndarray
                           Initial amplitudes of Voigt peaks.
        gauss_widths     : ndarray
                           Initial Gaussian widths of Voigt peaks.
        lorentz_widths   : ndarray
                           Initial Lorentzian widths of Voigt peaks.
        params           : ndarray
                           Array of initial parameters for least squares fitting.
        start_params     : list
                           Flattened list of initial parameters.
        decompositions   : list
                           List to store individual Voigt functions.
        '''
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
        '''
        Perform Voigt fitting using least squares optimization.

        Parameters:
        max_iter : int
                   Maximum number of iterations for fitting.

        Returns:
        error    : float
                   Mean absolute error of the fitting.

        Notes:
        Uses soft L1 loss and bounds parameters to constrain optimization.
        '''
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
        '''
        Calculate a Voigt profile using Faddeeva function approximation.

        Parameters:
        x            : ndarray
                       X values.
        center       : float
                       Center of the Voigt profile.
        amplitude    : float
                       Amplitude of the Voigt profile.
        gauss_width  : float
                       Gaussian component width of the Voigt profile.
        lorentz_width: float
                       Lorentzian component width of the Voigt profile.

        Returns:
        ndarray
        '''
        sigma = gauss_width / np.sqrt(2 * np.log(2))
        gamma = lorentz_width
        z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2) + 1e-20)
        return amplitude * np.real(wofz(z)).astype(float) / (sigma * np.sqrt(2 * np.pi) + 1e-20)

    def voigt_sum(self, x, params):
        '''
        Calculate the sum of Voigt profiles.

        Parameters:
        x      : ndarray
                 X values.
        params : ndarray
                 Array of parameters for Voigt profiles.

        Returns:
        ndarray
        '''
        params = params.tolist()
        params = [params[i:i + 4] for i in range(0, len(params), 4)]
        self.decompositions = [self.voigt(x, centre, amp, gw, lw) for centre, amp, gw, lw in params]
        return np.sum(self.decompositions, axis=0)

    def residual(self, params, x_vals, y_vals):
        '''
        Calculate residual between data and Voigt fit.

        Parameters:
        params : ndarray
                 Array of parameters for Voigt profiles.
        x_vals : ndarray
                 X values of the data.
        y_vals : ndarray
                 Y values of the data.

        Returns:
        ndarray
        '''
        return y_vals - self.voigt_sum(x_vals, params)