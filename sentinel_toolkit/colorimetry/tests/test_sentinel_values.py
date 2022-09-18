import unittest

import numpy as np
from colour import SpectralDistribution

from numpy.testing import assert_array_equal

from sentinel_toolkit.colorimetry import sd_to_sentinel_direct_colour, SpectralData, \
    sd_to_sentinel_direct_numpy, dn_to_sentinel


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

    _BANDS_DN = np.array([
        [
            [1872, 2192, 2024],
            [1616, 2064, 1864],
            [2192, 2448, 2392],
            [2352, 2512, 2568],
            [1840, 2096, 2072]
        ],
        [
            [2128, 2352, 2344],
            [2064, 2416, 2424],
            [2256, 2608, 2712],
            [2160, 2480, 2568],
            [1712, 1936, 1976]
        ],

        [
            [2064, 2224, 2200],
            [2320, 2512, 2520],
            [2128, 2256, 2344],
            [2064, 2224, 2328],
            [1744, 1936, 1896]
        ],
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    ]).astype(np.float32)
    _NODATA_VALUE = 0
    _BAND_OFFSETS = [-1000, -1000, -1000]
    _QUANTIFICATION_VALUE = 10000
    _NORMALIZED_SOLAR_IRRADIANCES = [1., 0.9312055109070034, 0.771930093124123]
    _EXPECTED_SENTINEL_RESPONSES = np.array([
        [
            [8.720000088214874, 11.099969566792216, 7.904563953904933],
            [6.159999966621399, 9.908026456216994, 6.66947617759235],
            [11.919999867677689, 13.48385648174483, 10.745267047202622],
            [13.519999384880066, 14.079826996329183, 12.10386400373938],
            [8.399999886751175, 10.206012407311341, 8.275090344311982]
        ],
        [
            [11.28000020980835, 12.589897934659614, 10.374740081662836],
            [10.639999806880951, 13.18586983684831, 10.992284257385496],
            [12.559999525547028, 14.973784155810058, 13.215443750093261],
            [11.59999966621399, 13.781841739037008, 12.10386400373938],
            [7.119999825954437, 8.716083345641772, 7.5340375634978844]
        ],
        [
            [10.639999806880951, 11.397955517886563, 9.26316091044169],
            [13.199999928474426, 14.079826996329183, 11.733337038199593],
            [11.28000020980835, 11.695940775178741, 10.374740081662836],
            [10.639999806880951, 11.397955517886563, 10.251231476571398],
            [7.440000027418137, 8.716083345641772, 6.916493387775224]
        ],
        [
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]
        ]
    ])

    def test_sd_to_sentinel_direct_colour(self):
        actual = sd_to_sentinel_direct_colour(self._SPECTRAL_DISTRIBUTION, self._BANDS_RESPONSES)
        assert_array_equal(self._EXPECTED_SENTINEL_RESPONSE, actual)

    def test_sd_to_sentinel_direct_numpy(self):
        spectral_data = SpectralData(self._SPECTRAL_DISTRIBUTION.wavelengths,
                                     self._SPECTRAL_DISTRIBUTION.values)
        actual = sd_to_sentinel_direct_numpy(spectral_data, self._BANDS_RESPONSES)
        assert_array_equal(self._EXPECTED_SENTINEL_RESPONSE, actual)

    def test_dn_to_sentinel(self):
        sentinel_responses = dn_to_sentinel(self._BANDS_DN,
                                            self._NODATA_VALUE,
                                            self._BAND_OFFSETS,
                                            self._QUANTIFICATION_VALUE,
                                            self._NORMALIZED_SOLAR_IRRADIANCES)
        assert_array_equal(self._EXPECTED_SENTINEL_RESPONSES, sentinel_responses)


if __name__ == '__main__':
    unittest.main()
