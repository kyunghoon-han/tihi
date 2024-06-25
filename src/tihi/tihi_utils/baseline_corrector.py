import numpy as np
from scipy import sparse
from scipy.signal import medfilt
from scipy.sparse.linalg import spsolve

def linear_baseline_correction(x_val, y_val, window_length=31, percentile=5):
    smoothed_data = medfilt(y_val, kernel_size=window_length)

    # Select baseline points based on a low percentile of the smoothed data
    threshold = np.percentile(smoothed_data, percentile)
    baseline_indices = np.where(smoothed_data <= threshold)[0]
    if len(baseline_indices) < 2:
        raise ValueError("Not enough points to fit a baseline. Adjust the percentile or window length.")
    
    baseline_indices = np.array(baseline_indices, dtype=int)    
    baseline_x = np.array(x_val)[baseline_indices.astype(int)]
    baseline_y = smoothed_data[baseline_indices]

    # Fit a linear function (y = mx + c) to the baseline points
    m, c = np.polyfit(baseline_x, baseline_y, 1)
    corrected_baseline = m * np.array(x_val) + c

    return corrected_baseline


def airPLS(y, lambda_=100, niter=15):
    '''
    AirPLS baseline correction algorithm.
    
    y      : input signal (spectral data)
    lambda_: parameter controlling the smoothness of the baseline
    niter  : maximum number of iterations
    
    Returns:
    baseline-corrected signal
    '''
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
    W = np.ones(L)
    for i in range(niter):
        Z = sparse.spdiags(W, 0, L, L)
        C = Z + lambda_ * D.dot(D.transpose())
        baseline = spsolve(C, Z.dot(y))
        W = np.abs(y - baseline) < 2 * np.sqrt(np.median((y - baseline) ** 2))
    
    return baseline

def arPLS(y, ratio=1e-6, lam=100, niter=100, full_output=False):
    L = len(y)

    diag = np.ones(L - 2)
    D = sparse.spdiags([diag, -2*diag, diag], [0, -1, -2], L, L - 2)

    H = lam * D.dot(D.T)  # The transposes are flipped w.r.t the Algorithm on pg. 252

    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)

    crit = 1
    count = 0

    while crit > ratio:
        baseline = spsolve(W + H, W * y)
        d = y - baseline
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
        return baseline, d, info
    else:
        return baseline