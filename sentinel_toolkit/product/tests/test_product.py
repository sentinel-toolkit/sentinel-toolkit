import os
import unittest
from pathlib import Path

import numpy as np
from numpy.testing import assert_array_equal
from rasterio import CRS
from rasterio._base import Profile, Affine

from sentinel_toolkit.product import S2Product


class TestProduct(unittest.TestCase):
    _PRODUCT_DIRECTORY_NAME = os.path.join(
        os.path.dirname(__file__),
        "test_data",
        "S2B_MSIL2A_20220915T092029_N0400_R093_T34TGN_20220915T112452.SAFE"
    )
    _METADATA_FILENAME = os.path.join(_PRODUCT_DIRECTORY_NAME, "MTD_MSIL2A.xml")

    _BAND_ID_1 = 1
    _BAND_ID_2 = 2
    _BAND_ID_3 = 3
    _BAND_IDS = [_BAND_ID_1, _BAND_ID_2, _BAND_ID_3]
    _BAND_ID_TO_FILENAME = {
        _BAND_ID_1: os.path.join(
            _PRODUCT_DIRECTORY_NAME,
            "GRANULE",
            "L2A_T34TGN_A028862_20220915T092030",
            "IMG_DATA",
            "R10m",
            "T34TGN_20220915T092029_B02_10m.jp2"
        ),
        _BAND_ID_2: os.path.join(
            _PRODUCT_DIRECTORY_NAME,
            "GRANULE",
            "L2A_T34TGN_A028862_20220915T092030",
            "IMG_DATA",
            "R10m",
            "T34TGN_20220915T092029_B03_10m.jp2"
        ),
        _BAND_ID_3: os.path.join(
            _PRODUCT_DIRECTORY_NAME,
            "GRANULE",
            "L2A_T34TGN_A028862_20220915T092030",
            "IMG_DATA",
            "R10m",
            "T34TGN_20220915T092029_B04_10m.jp2"
        ),
    }
    _OUT_SHAPE = (4, 5)
    _EXPECTED_PROFILE = Profile(
        {
            'driver': 'GTiff',
            'dtype': 'uint8',
            'nodata': None,
            'width': 5,
            'height': 4,
            'count': 3,
            'crs': CRS.from_epsg(32634),
            'transform': Affine(10.0, 0.0, 710480.0, 0.0, -10.0, 4690230.0),
            'tiled': False
        }
    )

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

    def setUp(self):
        self.product = S2Product(self._PRODUCT_DIRECTORY_NAME)

    def test_get_directory_name(self):
        actual = self.product.get_directory_name()
        self.assertEqual(self._PRODUCT_DIRECTORY_NAME, actual)

    def test_get_metadata(self):
        metadata = self.product.get_metadata()
        actual = metadata.get_filename()
        self.assertEqual(self._METADATA_FILENAME, actual)

    def test_get_dn_source(self):
        expected = self._BAND_ID_TO_FILENAME[self._BAND_ID_1]
        source = self.product.get_dn_source(self._BAND_ID_1)
        actual = str(Path(source.name))
        self.assertEqual(expected, actual)

    def test_get_band_id_to_dn_source(self):
        band_id_to_source = self.product.get_band_id_to_dn_source(self._BAND_IDS)
        actual = {band_id: str(Path(source.name))
                  for band_id, source in band_id_to_source.items()}

        self.assertEqual(self._BAND_ID_TO_FILENAME, actual)

    def test_dn_to_sentinel(self):
        profile, responses = self.product.dn_to_sentinel(self._BAND_IDS, out_shape=self._OUT_SHAPE)
        self.assertEqual(self._EXPECTED_PROFILE, profile)
        assert_array_equal(self._EXPECTED_SENTINEL_RESPONSES, responses)


if __name__ == '__main__':
    unittest.main()
