"""
s2_srf_reader provides the class S2SrfReader that acts as a python wrapper
of the Sentinel-2 Spectral Response Functions Excel file.
"""

import warnings

import pandas as pd

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


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

    def __init__(self, filename, satellite="A"):
        self.all_band_names = list(map(lambda b: b.format(satellite), self._BAND_NAMES))
        self.s2_srf_data = pd.read_excel(filename, sheet_name=self._SHEET_NAME.format(satellite))

    def get_wavelengths(self):
        """
        Retrieves the wavelengths.

        Returns
        -------
        output : ndarray
                 An array containing the wavelengths
        """
        return self.s2_srf_data[self._WAVELENGTH_NAME].to_numpy()

    def get_band_responses(self, band_name, wavelength_range=(360, 830)):
        """
        Retrieves the band responses given a band name.

        Parameters
        ----------
        band_name : str
                    The band name of interest.
        wavelength_range : tuple of int
               The wavelength range of interest. If missing, default to (360, 830).

        Returns
        -------
        output : ndarray
                 An array containing spectral responses of the given band.
        """
        wavelengths = self.get_wavelengths()
        mask = (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])

        return self.s2_srf_data[band_name].to_numpy()[mask]

    def get_bands_responses(self, band_names=None, wavelength_range=(360, 830)):
        """
        Retrieves the bands responses given an array of band names.

        Parameters
        ----------
        band_names : list of str
                     The band names of interest. If missing, default to all band names.

        wavelength_range : tuple of int
                           The wavelength range of interest. If missing, default to (360, 830).
        Returns
        -------
        output : ndarray
                 A (band_names_size x wavelengths_size) array
                 containing the spectral responses of the given bands.
        """
        if band_names is None:
            band_names = self.all_band_names

        wavelengths = self.get_wavelengths()
        mask = (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])

        return self.s2_srf_data[band_names].T.to_numpy()[:, mask]

    def get_all_band_names(self):
        """
        Retrieves all the band names.

        Returns
        -------
        output : list
                 A list containing all the band names.
        """
        return self.all_band_names
