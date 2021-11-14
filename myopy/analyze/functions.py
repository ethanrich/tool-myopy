

from scipy.signal import find_peaks
import numpy as np

def nalimov(x):
	"""
	Perform the Nalimov outlier test on a 1D array of data. For more info about the test:
	http://www.statistics4u.com/fundstat_eng/ee_nalimov_outliertest.html
	"""
    x_hat = np.mean(x)
    s = np.std(x)
    n = len(x)
    nals = []
    for i in range(n):
        nals.append((abs(x[i]-x_hat)/s) * (np.sqrt(n/(n-1))))
    
    nals = np.array(nals)
    threshold = np.sort(nals)[-10:][0] # smallest std value of the ten highest
    return np.where( nals > threshold)[0]

def clean_artefact_data(data, fs=1000, freq=50):
	"""
	Remove a periodic artefact from the data (such as FES artefact)
	"""

    # general forward comb filter
    b =  1
    L = fs//freq
    
    filtered_data = np.zeros(len(data))
    for i in range(L, len(data)):
        filtered_data[i] = (data[i] - b*data[i-L])
    baseline_corrected = abs(filtered_data - np.mean(filtered_data))
    
    # find the peaks
    peaks = find_peaks(baseline_corrected, distance=10)[0]
 
    # remove the peaks
    for p in peaks:
        baseline_corrected[p-3:p+3] = 0
    
    # nalimov the leftover artefact pulses
    nals = nalimov(baseline_corrected)
    
    # remove the nals
    for n in nals:
        baseline_corrected[n-3:n+3] = 0
    
    return baseline_corrected


def filtrect(data, fs=1000, low_band=1, high_band=499, rectify=True, line_noise=50):
    """
    Filters and potentially rectifies passed data
    
    Parameters
    ----------
    data: numpy array
        EMG data (time samples must be last dimension)
    fs: int
        sampling frequency, the default is 1000 Hz.
    high: int
        high-pass cut off frequency, the default is 30 Hz.
    low:int
        low-pass cut off frequency, the default is 400 Hz.
    rectify: bool
        determines whether the data should be rectified, the default is True
    line_noise: int
    	line noise frequency to remove

    Returns
    -------
    filtered data: array
        filtered data, if rectify == True data is also rectified

    """
    
	b, a = iircomb(line_noise, 5.0, fs=fs)
	filt_data = filtfilt(b, a, data)

	high = high_band/(fs/2)
	low = low_band/(fs/2)
	b1, a1    = butter(4, [low,high], btype='bandpass')
	filt_data2 = filtfilt(b1, a1, filt_data)

	if rectify == True:
	    filt_data2 = abs(filt_data2)
	return filt_data2



def rms(data):
    """
    Caluculates the root mean square

    Parameters
    ----------
    data : numpy array
        The data of which the rms is to be calculated over

    Returns
    -------
    The root mean square of the data

    """
    return np.sqrt(np.mean(data**2))

def mav(data):
    """
    calculates the mean absolute value

    Parameters
    ----------
    data : numpy array
        The data of which the mean absolute value should be calculated

    Returns
    -------
    mean absolute value, always positive

    """
    return np.mean(np.absolute(data), axis=0)


def max(data):
    """
    calculates the number of slope sign changes 
    
    Parameters
    ----------
    data : numpy array
        The numpy array of which the maximum value should be calculated

    Returns
    -------
    max : int
        maximum value of data

    """
    return np.max(data) 

def mad(data):
    """
    calculates the median absolute deviation
    
    Parameters
    ----------
    data : numpy array
        The numpy array of which the median absolute deviation should be calculated

    Returns
    -------
    int
        median absolute deviation

    """
    return median_abs_deviation(data)


def wfl(data):
    """
    calculates the waveform length
    
    Parameters
    ----------
    data : numpy array
        The numpy array of which the wave form length should be calculated

    Returns
    -------
    int
        wave form length

    """
    return np.sum(np.absolute(np.diff(data, axis=0)), axis=0)


def tkeo(data):
    """
	Calculates the TKEO of a given recording by using 2 samples.
	See Li et al., 2007

    Parameters
    ----------
    data : numpy array
        a 1D numpy array

    Returns
    -------
    numpy array
    	the tkeo 

    """

    i = data[1:-1] * data[1:-1]
    j = data[2:] * data[:-2]
	return i - j
