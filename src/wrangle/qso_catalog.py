# -*- coding: utf-8 -*-
"""
============================================
Data Wrangling Functions for non BAL quasars
============================================
"""

from attrs import define, Factory
import pandas as pd
import numpy as np
from astropy.table import Table
from astropy.io import fits

from src.utils import get_data_home

# with_logger = utility.with_logger(prefix_name=__name__)

nonbal_qso_col_l = ['SDSS_NAME', 'RA', 'DEC', 'PLATE', 'MJD', 'FIBERID', 'AUTOCLASS_PQN', 'Z', 'BAL_PROB', 'BI_CIV', 'AI_CIV']


@define
class QsoDataset:
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
    q_cat_path: str = None
    bal_prob_max: float = 0.0
    bal_prob_min: float = 0.0
    z_warning_max: float = 0.0  
    n: int = 8000
    random_state: int = 1234
    col_l: list[str] = Factory(nonbal_qso_col_l)

    




