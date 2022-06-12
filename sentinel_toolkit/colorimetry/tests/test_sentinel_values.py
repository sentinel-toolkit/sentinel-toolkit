import unittest

import numpy as np
from colour import SpectralDistribution

from sentinel_toolkit.colorimetry import sd_to_sentinel_direct_colour, sd_to_sentinel_direct_numpy

from numpy.testing import assert_array_equal

from sentinel_toolkit.colorimetry.sentinel_values import SpectralData


class TestSentinelValues(unittest.TestCase):
    _DB_FILENAME = "ecostress.db"
    _ECOSTRESS_DATA_DIRECTORY = "ecospeclib-all"

    _SPECTRAL_DISTRIBUTION = SpectralDistribution(
        {
            438: 0.104,
            439: 0.1042,
            440: 0.1043,
            441: 0.1044,
            442: 0.1045,
            443: 0.1046
        }
    )

    _BANDS_RESPONSES = np.array([
        [0.810893815261278, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.824198756004815, 0.010315428586995, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.854158107215052, 0.0300419331664615, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.870790876711332, 0.0268758905675229, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.887310969404313, 0.0241431503861076, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0.926199242291321, 0.0202100642531871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]).T

    _EXPECTED_SENTINEL_RESPONSE = [10.985433231270072, 11.086160373966965, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_sd_to_sentinel_direct_colour(self):
        actual = sd_to_sentinel_direct_colour(self._SPECTRAL_DISTRIBUTION, self._BANDS_RESPONSES)
        assert_array_equal(self._EXPECTED_SENTINEL_RESPONSE, actual)

    def test_sd_to_sentinel_direct_numpy(self):
        spectral_data = SpectralData(self._SPECTRAL_DISTRIBUTION.wavelengths,
                                     self._SPECTRAL_DISTRIBUTION.values)
        actual = sd_to_sentinel_direct_numpy(spectral_data, self._BANDS_RESPONSES)
        assert_array_equal(self._EXPECTED_SENTINEL_RESPONSE, actual)


if __name__ == '__main__':
    unittest.main()
