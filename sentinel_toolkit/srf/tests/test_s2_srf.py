import os
import unittest

import numpy as np
from colour import MultiSpectralDistributions
from numpy.testing import assert_array_equal

from sentinel_toolkit.srf import S2Srf
from sentinel_toolkit.srf import S2SrfOptions


class TestS2Srf(unittest.TestCase):
    _SRF_FILENAME = os.path.dirname(__file__) + "/test_data/s2a_srf.xlsx"

    _B1_NAME = "S2A_SR_AV_B1"
    _B1_INDEX = 0

    _B2_NAME = "S2A_SR_AV_B2"
    _B2_INDEX = 1

    _EXPECTED_BANDS_RESPONSES_DISTRIBUTION = MultiSpectralDistributions(
        {
            438: (0.810893815261278, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            439: (0.824198756004815, 0.010315428586995, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            440: (0.854158107215052, 0.0300419331664615, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            441: (0.870790876711332, 0.0268758905675229, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            442: (0.887310969404313, 0.0241431503861076, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            443: (0.926199242291321, 0.0202100642531871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        }
    )

    _WAVELENGTH_RANGE = (438, 439)

    _EXPECTED_ALL_BAND_NAMES = ["S2{}_SR_AV_B1",
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

    def setUp(self):
        self.s2_srf = S2Srf(self._SRF_FILENAME)

    def test_get_wavelengths(self):
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.wavelengths
        actual = self.s2_srf.get_wavelengths()
        assert_array_equal(expected, actual)

    def test_get_all_bands_responses(self):
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values.T
        actual = self.s2_srf.get_bands_responses()
        assert_array_equal(expected, actual)

    def test_get_bands_responses_satellite(self):
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values.T
        actual = self.s2_srf.get_bands_responses(S2SrfOptions(satellite='B'))
        assert_array_equal(expected, actual)

    def test_get_specific_bands_responses_with_bands(self):
        b1_values = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[:, self._B1_INDEX]
        b2_values = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[:, self._B2_INDEX]

        expected = np.array([b1_values, b2_values])
        actual = self.s2_srf.get_bands_responses(S2SrfOptions(band_ids=[self._B1_INDEX, self._B2_INDEX]))
        assert_array_equal(expected, actual)

    def test_get_bands_responses_with_wavelength_range(self):
        wavelengths = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.wavelengths
        mask = (wavelengths >= self._WAVELENGTH_RANGE[0]) & (wavelengths <= self._WAVELENGTH_RANGE[1])
        expected = self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION.values[mask].T

        actual = self.s2_srf.get_bands_responses(S2SrfOptions(wavelength_range=self._WAVELENGTH_RANGE))
        assert_array_equal(expected, actual)

    def test_get_all_bands_names_satellite_A(self):
        expected_band_names = list(map(lambda b: b.format('A'), self._EXPECTED_ALL_BAND_NAMES))
        actual = self.s2_srf.get_band_names()
        assert_array_equal(expected_band_names, actual)

    def test_get_bands_names_satellite_A(self):
        band_ids = [1, 2, 3]
        expected_band_names = np.array(list(map(lambda b: b.format('A'), self._EXPECTED_ALL_BAND_NAMES)))[band_ids]
        actual = self.s2_srf.get_band_names(band_ids)
        assert_array_equal(expected_band_names, actual)

    def test_get_all_bands_names_satellite_B(self):
        expected_band_names = list(map(lambda b: b.format('B'), self._EXPECTED_ALL_BAND_NAMES))
        actual = self.s2_srf.get_band_names(satellite='B')
        assert_array_equal(expected_band_names, actual)

    def test_get_bands_names_satellite_B(self):
        band_ids = [1, 2, 3]
        expected_band_names = np.array(list(map(lambda b: b.format('B'), self._EXPECTED_ALL_BAND_NAMES)))[band_ids]
        actual = self.s2_srf.get_band_names(band_ids, satellite='B')
        assert_array_equal(expected_band_names, actual)

    def test_get_bands_responses_distribution_satellite_A(self):
        actual = self.s2_srf.get_bands_responses_distribution()
        self.assertEqual(self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION, actual)

    def test_get_bands_responses_distribution_satellite_B(self):
        actual = self.s2_srf.get_bands_responses_distribution(S2SrfOptions(satellite='B'))
        self.assertEqual(self._EXPECTED_BANDS_RESPONSES_DISTRIBUTION, actual)


if __name__ == '__main__':
    unittest.main()
