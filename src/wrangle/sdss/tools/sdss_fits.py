"""
Tools to download and process SDSS fits files.

More information can be found at
http://www.sdss.org/dr7/products/spectra/index.html
"""
import gc  # garbage collection
import numpy as np
from scipy.ndimage import gaussian_filter1d, uniform_filter1d
from scipy import interpolate

from src.wrangle.sdss.tools.download import download_with_progress_bar

# This is the URL of the sdss fits spectra
# FITS_FILENAME = 'spSpec-%(mjd)05i-%(plate)04i-%(fiber)03i.fit'
# SDSS_URL = ('http://das.sdss.org/spectro/1d_26/%(plate)04i/'
#             '1d/spSpec-%(mjd)05i-%(plate)04i-%(fiber)03i.fit')

sdss_url_d = {
    'DR16': {
        'url':('https://data.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/%(plate)04i/'
            'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits'),
        'filename':'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits'
    },
    'DR14': {
        'url': ('https://data.sdss.org/sas/dr14/eboss/spectro/redux/v5_10_0/%(plate)04i/v5_10_0/'
            'spZbest-%(plate)04i-%(mjd)05i.fits'),
        'filename':'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits'
    },
    'DR12': {
        'url': ('https://data.sdss.org/sas/dr14/sdss/spectro/redux/v5_10_0/%(plate)04i/v5_10_0/'
            'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits'),
        'filename':'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits'      
    }
}

SDSS_URL = ('https://data.sdss.org/sas/dr16/eboss/spectro/redux/v5_13_0/spectra/lite/%(plate)04i/'
            'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits')
FITS_FILENAME = 'spec-%(plate)04i-%(mjd)05i-%(fiber)04i.fits'

# lines used to generate line-index labeling
LINES = dict(Ha=6564.61,
             Hb=4862.68,
             OI=6302.05,
             OIII=5008.24,
             NIIa=6549.86,
             NIIb=6585.27,
             SIIa=6718.29,
             SIIb=6732.67)


def sdss_fits_url(plate, mjd, fiber, sdss_dr='DR16'):
    """Return the URL of the spectrum FITS file"""
    return sdss_url_d[sdss_dr]['url'] % dict(plate=plate, mjd=mjd, fiber=fiber)


def sdss_fits_filename(plate, mjd, fiber, sdss_dr='DR16'):
    """Return the name of the spectrum FITS file"""
    return sdss_url_d[sdss_dr]['filename'] % dict(plate=plate, mjd=mjd, fiber=fiber)
