import unittest
from unittest.mock import patch

import numpy as np
from spectral import EcostressDatabase
from spectral.database.aster import Signature

from sentinel_toolkit.ecostress import Ecostress

from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal


class TestEcostress(unittest.TestCase):
    _DB_FILENAME = "ecostress.db"
    _ECOSTRESS_DATA_DIRECTORY = "ecospeclib-all"

    _QUERY = """
        select SpectrumID 
        from Spectra
        where MinWaveLength <= ? and MaxWaveLength >= ?
         """

    _SPECTRUM_ID = 0

    _SIGNATURE_LEN_6 = Signature()
    _SIGNATURE_LEN_6.x = np.array([0.438, 0.439, 0.440, 0.441, 0.442, 0.443])
    _SIGNATURE_LEN_6.y = np.array([10.4000, 10.4200, 10.4300, 10.4400, 10.4500, 10.4600])

    _SIGNATURE_LEN_7 = Signature()
    _SIGNATURE_LEN_7.x = np.array([0.438, 0.439, 0.440, 0.441, 0.442, 0.443, 0.444])
    _SIGNATURE_LEN_7.y = np.array([10.4000, 10.4200, 10.4300, 10.4400, 10.4500, 10.4600, 10.4800])

    @patch.object(EcostressDatabase, 'query')
    def test_get_spectrum_ids(self, mock_ecostress_database_query):
        ecostress = Ecostress(EcostressDatabase())
        ecostress.get_spectrum_ids()
        mock_ecostress_database_query.assert_called_once_with(self._QUERY, (0.83, 0.36))

    @patch.object(EcostressDatabase, 'query')
    def test_get_spectrum_ids_with_wavelength_range(self, mock_ecostress_database_query):
        ecostress = Ecostress(EcostressDatabase())
        ecostress.get_spectrum_ids(wavelength_rage=(420, 440))
        mock_ecostress_database_query.assert_called_once_with(self._QUERY, (0.44, 0.42))

    @patch.object(EcostressDatabase, 'get_signature')
    def test_get_spectral_distribution_colour(self, mock_ecostress_db):
        mock_ecostress_db.get_signature.return_value = self._SIGNATURE_LEN_6

        ecostress = Ecostress(mock_ecostress_db)
        sd = ecostress.get_spectral_distribution_colour(self._SPECTRUM_ID)

        assert_array_equal(self._SIGNATURE_LEN_6.x * 1000, sd.wavelengths)
        assert_array_almost_equal(self._SIGNATURE_LEN_6.y / 100, sd.values)

    @patch.object(EcostressDatabase, 'get_signature')
    def test_get_spectral_distribution_colour_with_wavelength_range(self, mock_ecostress_db):
        mock_ecostress_db.get_signature.return_value = self._SIGNATURE_LEN_7

        ecostress = Ecostress(mock_ecostress_db)
        sd = ecostress.get_spectral_distribution_colour(self._SPECTRUM_ID, wavelength_rage=(438, 443))

        assert_array_equal(self._SIGNATURE_LEN_7.x[0:-1] * 1000, sd.wavelengths)
        assert_array_almost_equal(self._SIGNATURE_LEN_7.y[0:-1] / 100, sd.values)

    @patch.object(EcostressDatabase, 'get_signature')
    def test_get_spectral_distribution_numpy(self, mock_ecostress_db):
        mock_ecostress_db.get_signature.return_value = self._SIGNATURE_LEN_6

        ecostress = Ecostress(mock_ecostress_db)
        sd = ecostress.get_spectral_distribution_colour(self._SPECTRUM_ID)

        assert_array_equal(self._SIGNATURE_LEN_6.x * 1000, sd.wavelengths)
        assert_array_almost_equal(self._SIGNATURE_LEN_6.y / 100, sd.values)

    @patch.object(EcostressDatabase, 'get_signature')
    def test_get_spectral_distribution_numpy_with_wavelength_range(self, mock_ecostress_db):
        mock_ecostress_db.get_signature.return_value = self._SIGNATURE_LEN_7

        ecostress = Ecostress(mock_ecostress_db)
        wavelengths, spectral_responses = ecostress.get_spectral_distribution_numpy(self._SPECTRUM_ID,
                                                                                    wavelength_rage=(438, 443))

        assert_array_equal(self._SIGNATURE_LEN_7.x[0:-1] * 1000, wavelengths)
        assert_array_almost_equal(self._SIGNATURE_LEN_7.y[0:-1] / 100, spectral_responses)


if __name__ == '__main__':
    unittest.main()
