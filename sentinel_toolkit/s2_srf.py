"""
s2_srf provides the method read_s2_srf that reads the S2_SRF functions from a given
Excel file and returns a corresponding colour.SpectralDistribution object that can be
used in other colour-science operations.
"""

import warnings

import numpy as np
import pandas as pd
from colour import MultiSpectralDistributions

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

_WAVELENGTH_NAME = "SR_WL"
_BAND_NAMES = ["S2{}_SR_AV_B1",
               "S2{}_SR_AV_B2",
               "S2{}_SR_AV_B3",
               "S2{}_SR_AV_B4",
               "S2{}_SR_AV_B5",
               "S2{}_SR_AV_B6",
               "S2{}_SR_AV_B7",
               "S2{}_SR_AV_B8",
               "S2{}_SR_AV_B8A",
               "S2{}_SR_AV_B9",
               "S2{}_SR_AV_B10",
               "S2{}_SR_AV_B11",
               "S2{}_SR_AV_B12"]
_SHEET_NAME = "Spectral Responses (S2{})"


def read_s2_srf(filename, satellite="A", shape=(360, 830)):
    """
    Read the Sentinel-2 spectral response functions excel file
    and return it as a colour.MultiSpectralDistributions object

    Parameters
    ----------
    filename : str
               The S2_SRF excel filename.
    satellite : str
                The satellite identifier - A or B.
    shape : tuple of int
            The wavelength range of interest represented as a tuple (start, end).
    Returns
    -------
    output : colour.MultiSpectralDistributions
             Returns the Sentinel-2 spectral response functions as
             a colour.MultiSpectralDistributions object.
    """
    srf_data = pd.read_excel(filename, sheet_name=_SHEET_NAME.format(satellite))

    wavelengths = srf_data[_WAVELENGTH_NAME]
    band_names = list(map(lambda b: b.format(satellite), _BAND_NAMES))

    bands_srf = srf_data[band_names][(wavelengths >= shape[0]) & (wavelengths <= shape[1])]
    bands_srf = np.stack(bands_srf.to_numpy(dtype=np.float64), axis=0)

    return MultiSpectralDistributions(dict(zip(wavelengths, bands_srf)))
