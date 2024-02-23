# -*- coding: utf-8 -*-
"""
==================================================
Data Wrangling Functions for SDSS Quasars Catalogs
==================================================
"""

import os
from attrs import define, Factory
import pandas as pd
import numpy as np
from astropy.table import Table
from astropy.io import fits

from src.utils import get_data_home

# with_logger = utility.with_logger(prefix_name=__name__)

nonbal_qso_col_l = ['SDSS_NAME', 'RA', 'DEC', 'PLATE', 'MJD', 'FIBERID', 'AUTOCLASS_PQN', 'Z', 'BAL_PROB', 'BI_CIV', 'AI_CIV']

qso_catalog_wget_d = {
    'DR16':{
        'url':'https://data.sdss.org/sas/dr16/eboss/qso/DR16Q/DR16Q_v4.fits',
        'filename':'DR16Q_v4.fits',
        'col_l':['SDSS_NAME', 'RA', 'DEC', 'PLATE', 'MJD', 'FIBERID', 'AUTOCLASS_PQN', 'Z', 'BAL_PROB', 'BI_CIV', 'AI_CIV']
        },
    'DR14':{
        'url':'https://data.sdss.org/sas/dr16/eboss/qso/DR14Q/DR14Q_v4_4.fits',
        'filename':'DR14Q_v4_4.fits',
        'col_l':['SDSS_NAME', 'RA', 'DEC', 'PLATE', 'MJD', 'FIBERID', 'Z',  'BI_CIV']
        },
    'DR12':{
        'url':'https://data.sdss.org/sas/dr16/eboss/qso/DR12Q/DR12Q.fits',
        'filename':'DR12Q.fits',
        'col_l':['SDSS_NAME', 'RA', 'DEC', 'PLATE', 'MJD', 'FIBERID', 'Z', 'BAL_FLAG_VI', 'BI_CIV', 'AI_CIV']
        }
}



@define
class QsoCatalogDataset:
    """
    Wrangles a sample of the SDSS Quasar Catalog of choice

    Parameters
    ----------
    bal_prob_max : float, optional (default=0.0)
    bal_prob_min : float, optional (default=None)
    data_release : int, optional (default=16)

    Methods
    -------

    """

    data_release: int = 16
    sdss_dr: str = None
    q_cat_path: str = None
    col_l: list[str] = Factory(list)
    data_home: str = get_data_home()
    sdss_dr: str = None
    qso_catalog_wget_d: dict = qso_catalog_wget_d
    cat_filename: str = None
    overwrite: bool = False

    def __attrs_post_init__(self):
        self.sdss_dr = 'DR' + str(self.data_release)
        self.col_l.extend(self.qso_catalog_wget_d[self.sdss_dr]['col_l'])
        self.cat_filename = os.path.join(self.data_home,
                                         'sdss_quasar_catalogs',
                                         self.qso_catalog_wget_d[self.sdss_dr]['filename'])

    def download_cat_if_not_exist(self):
        if self.overwrite or not os.path.isfile(self.cat_filename):
            print('Quasar catalog file not found. Downloading now.')
            import urllib.request
            try:
                urllib.request.urlretrieve(self.qso_catalog_wget_d[self.sdss_dr]['url'], self.cat_filename)
                print('Download successful. File at {self.cat_filename}')
            except Exception as e:
                print('Download not successful.')
                raise e
        else:
            print('Quasar catalog found.')

    def get_qso_cat_samp(self, n=8000, bal_prob=None, bal_prob_max=None, z_warning_max=0.0, random_state=1234):
        hdul = fits.open(self.cat_filename)
        hdr = hdul[0].header
        dr16_data = hdul[1].data

        if bal_prob:
            bal_qso_mask = (bal_prob == dr16_data['BAL_PROB']) & \
                (dr16_data['zWarning'] <= z_warning_max)
        elif bal_prob_max:
            bal_qso_mask = (dr16_data['BAL_PROB'] <= bal_prob_max) & \
                (dr16_data['zWarning'] >= z_warning_max)         
        else:
            bal_qso_mask = (dr16_data['zWarning'] <= z_warning_max) 
        
        nonbal_qso_hdul = dr16_data[bal_qso_mask]

        nonbal_qso_df = Table(nonbal_qso_hdul)[self.col_l].to_pandas()
        nonbal_qso_df = nonbal_qso_df.sample(n, random_state=random_state).reset_index(drop=True)

        return nonbal_qso_df


    def run(self, n=8000, bal_prob=None, bal_prob_max=None, z_warning_max=0.0, random_state=1234):
        self.download_cat_if_not_exist()
        return self.get_qso_cat_samp(n=n, bal_prob=bal_prob, bal_prob_max=bal_prob_max, z_warning_max=z_warning_max, random_state=random_state)


    




