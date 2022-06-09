"""
This module contains the test for reading Sentinel-2 Spectral Response functions.
"""

import os

import unittest

from colour import MultiSpectralDistributions

from sentinel_toolkit import read_s2_srf


class TestS2Srf(unittest.TestCase):
    _SRF_FILENAME = os.path.dirname(__file__) + "/test_data/s2a_srf.xlsx"
    _EXPECTED_RESULT = MultiSpectralDistributions(
        {
            438: (0.810893815261278, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            439: (0.824198756004815, 0.010315428586995, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            440: (0.854158107215052, 0.0300419331664615, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            441: (0.870790876711332, 0.0268758905675229, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            442: (0.887310969404313, 0.0241431503861076, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            443: (0.926199242291321, 0.0202100642531871, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        }
    )

    def test_read_s2_srf(self):
        self.assertEqual(read_s2_srf(self._SRF_FILENAME), self._EXPECTED_RESULT)


if __name__ == '__main__':
    unittest.main()
