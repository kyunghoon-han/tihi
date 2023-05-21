import numpy as np

# the Cauchy distribution
def cauchy(x, mu, gamma):
    return gamma / (np.pi * ( (x-mu)**2 + gamma**2 ))

# when x = mu /pm delta_x
def cauchy_zero(delta_x, gamma):
    return gamma / (np.pi * (delta_x**2 + gamma**2))

# its derivative when x=mu
def cauchy_deriv(x, mu, gamma):
    up = - 2 * gamma * ( x - mu)
    down = np.pi * (mu * mu + gamma*gamma - 2 * mu * gamma + x * x)**2
    return up / down

def gamma_from_derivative(derivative):
    '''
        gamma_from_derivative
        returns the gamma from the input derivative

        arg:
            derivative : derivative at the centre of the distribution
    '''
    return 1/(np.pi * derivative)

def get_cauchy(xs, ys, y_diff, peak_indices):
    '''
        get_cauchy:
        returns a len(peak_indices) number of 
        Cauchy distributions meeting the criteria

        args:
            xs : dependent variable
            ys : independent variable
            y_diff: first derivative on ys
            peak_indices : indices where the peaks are
    '''
    list_cauchies = []
    for peak_index in peak_indices:
        gamma = gamma_from_derivative(y_diff[peak_index])
        y_cauchy= cauchy(xs, ys[peak_index], 1)
        y_cauchy = (y_cauchy - np.min(y_cauchy))/np.max(y_cauchy)
        list_cauchies.append(y_cauchy)
    return list_cauchies