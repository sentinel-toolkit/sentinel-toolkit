"""
s2_srf_reader provides the class S2SrfReader that acts as a python wrapper
of the Sentinel-2 Spectral Response Functions Excel file.
"""

import warnings

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd

from colour import MultiSpectralDistributions

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


@dataclass
class S2SrfOptions:
    """
    Keeps the options that can be passed to some of the S2Srf methods:
    (satellite, band_ids, wavelenegth_range)
    """
    satellite: str = 'A'
    band_ids: List[int] = None
    wavelength_range: Tuple[int, int] = (360, 830)

    def unpack(self):
        """
        Unpacks the dataclass into satellite, band_names and wavelength_range.
        Returns
        -------
        satellite : str
        band_ids : list of int
        wavelength_range : tuple of int
        """
        return self.satellite, self.band_ids, self.wavelength_range


class S2Srf:
    """
    Provides methods for reading the Sentinel-2 Spectral Response Functions Excel file.
    """

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

    def __init__(self, filename):
        self.all_band_names = {
            'A': np.array(list(map(lambda b: b.format('A'), self._BAND_NAMES))),
            'B': np.array(list(map(lambda b: b.format('B'), self._BAND_NAMES)))
        }

        self.s2_srf_data = {
            'A': pd.read_excel(filename, sheet_name=self._SHEET_NAME.format('A')),
            'B': pd.read_excel(filename, sheet_name=self._SHEET_NAME.format('B'))
        }

    def get_wavelengths(self, satellite='A'):
        """
        Retrieves the wavelengths.

        Parameters
        ----------
        satellite : str
                    The satellite of interest - A or B. If missing, default to 'A'
        Returns
        -------
        output : ndarray
                 An array containing the wavelengths
        """
        return self.s2_srf_data[satellite][self._WAVELENGTH_NAME].to_numpy()

    def get_bands_responses(self, options=None):
        """
        Retrieves the bands responses given an array of band names.

        Parameters
        ----------
        options : S2SrfOptions
                  The satellite, band names and wavelength range of interest.
                  If satellite is missing, satellite 'A' will be used.
                  If band ids are missing, all band ids will be used.
                  If wavelength range is missing, (360, 830) will be used.
        Returns
        -------
        output : ndarray
                 A (band_names_size x wavelengths_size) array
                 containing the spectral responses of the given bands.
        """
        satellite, band_ids, wavelength_range = self._parse_s2srf_options(options)

        wavelengths = self.get_wavelengths()
        mask = (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])
        band_names = self.get_band_names(band_ids, satellite)

        return self.s2_srf_data[satellite][band_names].T.to_numpy()[:, mask]

    def _parse_s2srf_options(self, options):
        if options is None:
            satellite, band_ids, wavelength_range = None, None, None
        else:
            satellite = options.satellite
            band_ids = options.band_ids
            wavelength_range = options.wavelength_range
        if satellite is None:
            satellite = 'A'
        if band_ids is None:
            band_ids = list(range(0, len(self._BAND_NAMES)))
        if wavelength_range is None:
            wavelength_range = (360, 830)

        return satellite, band_ids, wavelength_range

    def get_band_names(self, band_ids=None, satellite='A'):
        """
        Retrieves all the band names.

        Parameters
        ----------
        band_ids : list of int
                   The band ids of interest - 0 to 12. If missing, default to all bands.s
        satellite : str
                    The satellite of interest - A or B. If missing, default to 'A'
        Returns
        -------
        output : list
                 A list containing all the band names.
        """
        if band_ids is None:
            band_ids = list(range(0, len(self._BAND_NAMES)))
        return self.all_band_names[satellite][band_ids]

    def get_bands_responses_distribution(self, options=None):
        """
        Read the Sentinel-2 spectral response functions Excel file
        and return it as a colour.MultiSpectralDistributions object

        Parameters
        ----------
        options : S2SrfOptions
                  The satellite, band names and wavelength range of interest.
                  If satellite is missing, satellite 'A' will be used.
                  If band names are missing, all band names will be used.
                  If wavelength range is missing, (360, 830) will be used.
        Returns
        -------
        output : colour.MultiSpectralDistributions
                 The Sentinel-2 spectral response functions
                 as a colour.MultiSpectralDistributions object.
        """
        satellite, band_ids, wavelength_range = self._parse_s2srf_options(options)

        band_names = self.get_band_names(band_ids, satellite)

        wavelengths = self.get_wavelengths()
        mask = (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])
        wavelengths = wavelengths[mask]

        bands_srf = self.s2_srf_data[satellite][band_names].to_numpy()[mask, :]

        return MultiSpectralDistributions(dict(zip(wavelengths, bands_srf)))
