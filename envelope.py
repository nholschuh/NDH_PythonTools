import numpy as np 
import scipy as scp
import scipy.signal as signal


def envelope(record,real_or_abs=0):

    # Compute the analytic signal -- can only take the hilbert transform on real numbers
    if real_or_abs == 0:
        analytic_signal = signal.hilbert(np.real(record))
    else:
        analytic_signal = signal.hilbert(np.abs(record))
    return {'signal':analytic_signal,'envelope':np.abs(analytic_signal),'phase':np.angle(analytic_signal)}
