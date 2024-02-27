# -*- coding: utf-8 -*-
"""
===========================================
Data Wrangling Functions for quasar spectra
===========================================
"""

import os
from attrs import define, Factory
import pandas as pd
import numpy as np

from astropy.table import Table
from astropy.io import fits
from astropy import units as u
from specutils.manipulation import FluxConservingResampler
from specutils import Spectrum1D
from specutils.spectra.spectral_axis import SpectralAxis

from src.utils import get_data_home
from src.wrangle.sdss.tools.download import download_with_progress_bar
from src.wrangle.sdss.tools.sdss_fits import sdss_fits_url, sdss_fits_filename
from src.wrangle.sdss.tools.wavelengths import get_default_spectral_axis

spectral_axis = get_default_spectral_axis()

@define
class QsoSpectraDataset:
    """
    Wrangles spectra from a list of quasars

    Parameters
    ----------
    bal_prob_max : float, optional (default=0.0)
    bal_prob_min : float, optional (default=None)
    data_release : int, optional (default=16)

    Methods
    -------

    """

    data_release: int = 16
    data_home: str = get_data_home()

    def fetch_sdss_spectrum(self, plate, mjd, fiber, z, data_release=None,
                            data_home=None, download_if_missing=True,
                            cache_to_disk=True):
        """Fetch an SDSS spectrum from the Data Archive Server

        Parameters
        ----------
        plate: integer
            plate number of desired spectrum
        mjd: integer
            mean julian date of desired spectrum
        fiber: integer
            fiber number of desired spectrum

        Other Parameters
        ----------------
        data_home: string (optional)
            directory in which to cache downloaded fits files.  If not
            specified, it will be set to ~/astroML_data.
        download_if_missing: boolean (default = True)
            download the fits file if it is not cached locally.
        cache_to_disk: boolean (default = True)
            cache downloaded file to data_home.

        Returns
        -------
        spec: :class:`astroML.tools.SDSSfits` object
            An object wrapper for the fits data
        """
        data_home = get_data_home()
        if not data_release:
            data_release = self.data_release
        sdss_dr = 'DR' + str(data_release)
        target_url = sdss_fits_url(plate, mjd, fiber, sdss_dr=sdss_dr)

        target_file = os.path.join(data_home, 'SDSS', sdss_dr, '%04i' % plate,
                                sdss_fits_filename(plate, mjd, fiber))
        print(target_file)
        if not os.path.exists(target_file):
            if not download_if_missing:
                raise IOError("SDSS colors training data not found")
            print(target_url)
            buf = download_with_progress_bar(target_url, return_buffer=True)

            if cache_to_disk:
                print("caching to %s" % target_file)
                if not os.path.exists(os.path.dirname(target_file)):
                    os.makedirs(os.path.dirname(target_file))
                fhandler = open(target_file, 'wb')
                fhandler.write(buf.read())
                buf.seek(0)
        else:
            buf = target_file
        print(buf)
        spec = Spectrum1D.read(file_obj=buf, format="SDSS-III/IV spec")
        spec.set_redshift_to(z)
        return spec
    
    def get_shifted_and_rebinned_spec_l(self, df, spec_range=[1260,2400], redshift=0, cut_head_tail=False, clean_mask=True, data_release=None):
        fluxcon = FluxConservingResampler()
        if not data_release:
            data_release = self.data_release

        spec_l = []
        for idx, row in df.iterrows():
            spec = self.fetch_sdss_spectrum(row.PLATE, row.MJD, row.FIBERID, row.Z, data_release=data_release)
            spec.shift_spectrum_to(redshift=redshift)
            spec = spec[spec_range[0]*u.AA:spec_range[1]*u.AA]
            print(f'Processing spectrum {idx}')

            if not np.array_equal(spec.spectral_axis, spectral_axis):
                print('Resampling axis')
                spec = fluxcon(spec, spectral_axis)
            if cut_head_tail:
                spec = spec[1:-1]
            if clean_mask:
                spec.mask = np.full((len(spec.spectral_axis)), False)
            spec_l.append(spec)
        return spec_l

