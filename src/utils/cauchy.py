import numpy as np

# the Cauchy distribution
def cauchy(x, mu, gamma):
    return gamma / (np.pi * ( (x-mu)**2 + gamma**2 ))

# when x = mu
def cauchy_zero(gamma):
    return gamma / (np.pi * gamma**2)

# its derivative when x=mu
def cauchy_deriv(x, mu, gamma):
    up = - 2 * gamma * ( x - mu)
    down = np.pi * (mu * mu + gamma*gamma - 2 * mu * gamma + x * x)**2
    return up / down

def get_gamma(peak_y):
    '''
        get_gamma
        obtain gamma from the peak

        arg:
            peak_y : value of the peak
    '''
    return 1/(np.pi * peak_y)

def get_amplitude(gamma, peak_y):
    return peak_y / cauchy_zero(gamma) # this will just be 1/pi

def get_cauchy(xs, ys, peak_indices):
    '''
        get_cauchy:
        returns a len(peak_indices) number of 
        Cauchy distributions meeting the criteria

        args:
            xs : dependent variable
            ys : independent variable
            peak_indices : indices where the peaks are
    '''
    list_cauchies = []
    list_amps = []
    list_gammas = []
    list_centres = []
    sum_cauchy = np.zeros_like(xs)
    for peak_index in peak_indices:
        gamma = get_gamma(ys[peak_index])
        amp = get_amplitude(gamma, ys[peak_index])
        y_cauchy= cauchy(xs, xs[peak_index], gamma) * amp
        list_cauchies.append(y_cauchy)
        sum_cauchy = sum_cauchy + y_cauchy
        list_amps.append(amp)
        list_gammas.append(gamma)
        list_centres.append(xs[peak_index])
    #sum_cauchy = (sum_cauchy - np.min(sum_cauchy))/np.max(sum_cauchy)
    return list_cauchies, sum_cauchy, [list_centres, list_amps, list_gammas]