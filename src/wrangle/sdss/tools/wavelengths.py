import numpy as np
from src.utils import get_data_home
from astropy import units as u
from specutils.spectra.spectral_axis import SpectralAxis


def get_default_wavelengths():
    data_home = get_data_home()
    wavelength_path = data_home + '/wavelengths.txt'
    wavelengths = np.loadtxt(wavelength_path, delimiter=",")
    return wavelengths

def get_default_spectral_axis():
    wavelengths = get_default_wavelengths()
    spectral_axis = SpectralAxis(wavelengths*u.AA)
    return spectral_axis