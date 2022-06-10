import os
import unittest

import numpy as np
from numpy.testing import assert_array_equal

from sentinel_toolkit import S2Srf


class TestS2Srf(unittest.TestCase):
    _SRF_FILENAME = os.path.dirname(__file__) + "/test_data/s2a_srf.xlsx"

    _B1_NAME = "S2A_SR_AV_B1"
    _B2_NAME = "S2A_SR_AV_B2"

    _WAVELENGTH_RANGE = (438, 439)

    _EXPECTED_WAVELENGTHS = [438, 439, 440, 441, 442, 443]
    _EXPECTED_B1_RESPONSES = [0.810893815261278,
                              0.824198756004815,
                              0.854158107215052,
                              0.870790876711332,
                              0.887310969404313,
                              0.926199242291321]
    _EXPECTED_B2_RESPONSES = [0,
                              0.010315428586995,
                              0.0300419331664615,
                              0.0268758905675229,
                              0.0241431503861076,
                              0.0202100642531871]
    _EXPECTED_ALL_BAND_NAMES = ["S2A_SR_AV_B1",
                                "S2A_SR_AV_B2",
                                "S2A_SR_AV_B3",
                                "S2A_SR_AV_B4",
                                "S2A_SR_AV_B5",
                                "S2A_SR_AV_B6",
                                "S2A_SR_AV_B7",
                                "S2A_SR_AV_B8",
                                "S2A_SR_AV_B8A",
                                "S2A_SR_AV_B9",
                                "S2A_SR_AV_B10",
                                "S2A_SR_AV_B11",
                                "S2A_SR_AV_B12"]

    def test_get_wavelengths(self):
        actual = S2Srf(self._SRF_FILENAME).get_wavelengths()
        assert_array_equal(self._EXPECTED_WAVELENGTHS, actual)

    def test_get_band_responses(self):
        actual = S2Srf(self._SRF_FILENAME).get_band_responses(self._B1_NAME)
        assert_array_equal(self._EXPECTED_B1_RESPONSES, actual)

    def test_get_band_masked_responses(self):
        expected = self._EXPECTED_B1_RESPONSES[0:2]
        actual = S2Srf(self._SRF_FILENAME).get_band_responses(self._B1_NAME, wavelength_range=self._WAVELENGTH_RANGE)
        assert_array_equal(expected, actual)

    def test_get_bands_responses(self):
        expected = np.array([self._EXPECTED_B1_RESPONSES, self._EXPECTED_B2_RESPONSES])
        actual = S2Srf(self._SRF_FILENAME).get_bands_responses([self._B1_NAME, self._B2_NAME])
        assert_array_equal(expected, actual)

    def test_get_bands_masked_responses(self):
        expected = np.array([self._EXPECTED_B1_RESPONSES[0:2], self._EXPECTED_B2_RESPONSES[0:2]])
        actual = S2Srf(self._SRF_FILENAME).get_bands_responses([self._B1_NAME, self._B2_NAME],
                                                               wavelength_range=self._WAVELENGTH_RANGE)
        assert_array_equal(expected, actual)

    def test_get_all_bands_names(self):
        actual = S2Srf(self._SRF_FILENAME).get_all_band_names()
        assert_array_equal(self._EXPECTED_ALL_BAND_NAMES, actual)


if __name__ == '__main__':
    unittest.main()
