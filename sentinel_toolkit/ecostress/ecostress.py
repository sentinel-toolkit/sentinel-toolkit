"""
ecostress provides a wrapper class around the EcostressDatabase class from spectral library.
Ecostress wrapper class can be used for querying spectral data only in a given wavelength range
"""

import numpy as np

from colour import SpectralDistribution
from colour import SpectralShape
from scipy.interpolate import interp1d

from sentinel_toolkit.colorimetry.sentinel_values import SpectralData


class Ecostress:
    """
    Ecostress is a wrapper around the EcostressDatabase from spectral library.
    """

    def __init__(self, ecostress_db):
        self.ecostress_db = ecostress_db

    def get_spectrum_ids(self, wavelength_rage=(360, 830)):
        """
        Returns the spectrum identifiers of the ecostress examples
        that have some spectral data in the given wavelength_range.

        Parameters
        ----------
        wavelength_rage : tuple of int
                          The wavelength range of interest.

        Returns
        -------
        output : list of int
                 A list of the identifiers of the found examples.
        """
        sql = """
        select SpectrumID 
        from Spectra
        where MinWaveLength <= ? and MaxWaveLength >= ?
         """

        min_wavelength = wavelength_rage[0] / 1000
        max_wavelength = wavelength_rage[1] / 1000

        return self.ecostress_db.query(sql, (max_wavelength, min_wavelength)).fetchall()

    def get_spectral_distribution_colour(self, spectrum_id, wavelength_rage=(360, 830)):
        """
        Returns the SpectralDistribution of a given example
        by a given spectrum_id and wavelength_range.

        Parameters
        ----------
        spectrum_id : int
                      The spectrum identifier.
        wavelength_rage : tuple of int
                          The wavelength range of interest.

        Returns
        -------
        output : colour.SpectralDistribution
                 The corresponding SpectralDistribution.
        """
        signature = self.ecostress_db.get_signature(spectrum_id)

        wavelengths = np.round(np.array(signature.x), 4) * 1000
        spectral_responses = np.round(np.array(signature.y), 4) / 100

        spectral_data = dict(zip(wavelengths, spectral_responses))

        spectral_distribution = SpectralDistribution(spectral_data, name='Ecostress')
        shape = SpectralShape(wavelength_rage[0], wavelength_rage[1], 1)
        spectral_distribution.interpolate(shape)

        return spectral_distribution

    def get_spectral_distribution_numpy(self, spectrum_id, wavelength_rage=(360, 830)):
        """
        Returns the SpectralDistribution of a given example
        by a given spectrum_id and wavelength_range.
        This method can be used for gaining better performance
        if this method is called from a loop for a lot of examples.

        Parameters
        ----------
        spectrum_id : int
                      The spectrum identifier.
        wavelength_rage : tuple of int
                          The wavelength range of interest.

        Returns
        -------
        output : SpectralData (tuple)
                 The tupled wavelengths and spectral_responses
        """
        signature = self.ecostress_db.get_signature(spectrum_id)

        wavelengths = np.trunc(np.round(np.array(signature.x), 4) * 1000).astype(int)
        spectral_responses = np.round(np.array(signature.y), 4) / 100

        interpolator = interp1d(wavelengths, spectral_responses)

        min_wavelength = max(wavelengths[0], wavelength_rage[0])
        max_wavelength = min(wavelengths[-1], wavelength_rage[1])

        wavelengths = np.arange(min_wavelength, max_wavelength + 1, 1)
        spectral_responses = interpolator(wavelengths)

        return SpectralData(wavelengths, spectral_responses)
