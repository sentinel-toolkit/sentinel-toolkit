import os
import unittest

import numpy as np
from numpy.testing import assert_array_equal

from sentinel_toolkit.product.metadata import ProductMetadata


class TestProductMetadata(unittest.TestCase):
    _METADATA_FILENAME = os.path.dirname(__file__) + "/test_data/metadata.xml"

    _EXPECTED_SENSING_DATE = "2022-09-15"
    _EXPECTED_NODATA_VALUE = 0
    _EXPECTED_BOA_QUANTIFICATION_VALUE = 10000
    _EXPECTED_BAND_ID_TO_BOA_OFFSET = {
        0: -1000,
        1: -1000,
        2: -1000,
        3: -1000
    }
    _EXPECTED_BAND_ID_TO_SOLAR_IRRADIANCE = {
        0: 1874.3,
        1: 1959.75,
        2: 1824.93,
        3: 1512.79
    }

    def setUp(self):
        self.product_metadata = ProductMetadata(self._METADATA_FILENAME)

    def test_get_sensing_date(self):
        actual = self.product_metadata.get_sensing_data()
        self.assertEqual(self._EXPECTED_SENSING_DATE, actual)

    def test_get_nodata_value(self):
        actual = self.product_metadata.get_nodata_value()
        self.assertEqual(self._EXPECTED_NODATA_VALUE, actual)

    def test_get_boa_quantification_value(self):
        actual = self.product_metadata.get_boa_quantification_value()
        self.assertEqual(self._EXPECTED_BOA_QUANTIFICATION_VALUE, actual)

    def test_get_band_id_to_boa_offset(self):
        actual = self.product_metadata.get_band_id_to_boa_offset()
        self.assertEqual(self._EXPECTED_BAND_ID_TO_BOA_OFFSET, actual)

    def test_get_boa_offsets(self):
        band_ids = [1, 2, 3]
        expected = np.array([self._EXPECTED_BAND_ID_TO_BOA_OFFSET[band_id] for band_id in band_ids])
        actual = self.product_metadata.get_boa_offsets(band_ids)
        assert_array_equal(expected, actual)

    def test_get_band_id_to_solar_irradiance(self):
        actual = self.product_metadata.get_band_id_to_solar_irradiance()
        self.assertEqual(self._EXPECTED_BAND_ID_TO_SOLAR_IRRADIANCE, actual)

    def test_get_solar_irradiances(self):
        band_ids = [1, 2, 3]
        expected = np.array([self._EXPECTED_BAND_ID_TO_SOLAR_IRRADIANCE[band_id] for band_id in band_ids])
        actual = self.product_metadata.get_solar_irradiances(band_ids)
        assert_array_equal(expected, actual)

    def test_get_normalized_solar_irradiances(self):
        band_ids = [1, 2, 3]
        expected_solar_irradiance = np.array([self._EXPECTED_BAND_ID_TO_SOLAR_IRRADIANCE[band_id]
                                              for band_id in band_ids])
        expected = expected_solar_irradiance / np.max(expected_solar_irradiance)
        actual = self.product_metadata.get_normalized_solar_irradiances(band_ids)
        assert_array_equal(expected, actual)
