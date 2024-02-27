from scipy.signal import find_peaks, peak_widths
from astropy import units as u
from astropy.constants import c
import numpy as np


def get_bal_mask(flux, wavelength, rest_wavelength=1549.48, v_range=[-25000, 0], min_trough_depth=0.4, min_trough_width=2000, max_trough_width=25000, plt_return=False):
    # Finding the minimum limit to search for troughs i.e. blueshifts of up to -25,000km/s
    min_trough_lim = ( ( v_range[0]*u.km/u.s )/(c) + 1 ) * ( rest_wavelength * u.AA )
    min_trough_disp = rest_wavelength * u.AA - min_trough_lim

    # Finding the minimum limit to search for troughs i.e. blueshifts of up to -25,000km/s
    min_bal_lim = ( ( min_trough_width*u.km/u.s )/(c) + 1 ) * ( rest_wavelength * u.AA )
    min_bal_trough_width = np.abs(rest_wavelength * u.AA - min_bal_lim).value
    # Finding the max limit to search for troughs i.e. blueshifts of up to -25,000km/s
    max_bal_lim = ( ( max_trough_width*u.km/u.s )/(c) + 1 ) * ( rest_wavelength * u.AA )
    max_bal_trough_width = np.abs(rest_wavelength * u.AA - max_bal_lim).value

    # Finding the minimum limit to search for troughs i.e. blueshifts of up to -25,000km/s
    min_trough_lim = ( ( v_range[0]*u.km/u.s )/(c) + 1 ) * ( rest_wavelength * u.AA )
    min_trough_disp = (rest_wavelength * u.AA - min_trough_lim).value

    # Find indices corresponding to the region of interest
    civ_indices = np.where((wavelength >= (rest_wavelength - min_trough_disp)) &
                        (wavelength <= rest_wavelength))[0]

    # Extract wavelength and flux data within the defined window
    civ_wavelength = wavelength[civ_indices]
    civ_flux = flux[civ_indices]

    # Smooth the flux data to enhance peak detection
    smoothed_flux = np.convolve(civ_flux, np.ones(5)/5, mode='valid')

    # Find peaks (troughs) in the smoothed flux data
    trough_indices, _ = find_peaks(-smoothed_flux, prominence = 1.5, width=[min_bal_trough_width,max_bal_trough_width] )
    trough_widths, _, _, _ = peak_widths(-smoothed_flux, trough_indices, rel_height=1)

    if len(trough_indices) > 0:
        # Set the mask region
        min_mask_wavelength = civ_wavelength[trough_indices.min()] - trough_widths[trough_indices.argmin()]/2
        bal_wavelength_mask = [min_mask_wavelength, rest_wavelength]
        bal_idx_mask = [np.absolute(wavelength-bal_wavelength_mask[0]).argmin(), np.absolute(wavelength-bal_wavelength_mask[1]).argmin()]
        
    else:
        bal_wavelength_mask = None
        bal_idx_mask = None

    if plt_return:
        return bal_idx_mask, bal_wavelength_mask, wavelength, flux, civ_wavelength, smoothed_flux, civ_wavelength, trough_indices, trough_widths
    else:
        return bal_idx_mask
    

def get_bal_masks(X, wavelength, rest_wavelength=1549.48, v_range=[-25000, 0], min_trough_depth=0.4, min_trough_width=2000, max_trough_width=25000, plt_return=False):
    bal_masks = [get_bal_mask(X[i], wavelength) for i in range(len(X))]
    return bal_masks


def get_bal_masked_flux(X, X_replace, wavelength, rest_wavelength=1549.48, v_range=[-25000, 0], min_trough_depth=0.4, min_trough_width=2000, max_trough_width=25000, plt_return=False):
        bal_idx_mask = get_bal_masks(X, wavelength)
        for i in np.arange(0, len(X)):
            X[i][bal_idx_mask[i]] = X_replace[i][bal_idx_mask[i]]
        return X