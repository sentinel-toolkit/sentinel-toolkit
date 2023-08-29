import os
import unittest

from sentinel_toolkit.colorimetry import (
    get_illuminant_in_range,
    D65_360_830_1NM,
    get_well_known_illuminant,
    get_illuminant_from_file
)

_ILLUMINANT_DIRECTORY_NAME = os.path.join(os.path.dirname(__file__), "test_data")
_ILLUMINANT_FILENAME = os.path.join(_ILLUMINANT_DIRECTORY_NAME, "D65.1nm")


class TestIlluminants(unittest.TestCase):
    def test_get_illuminant_in_range(self):
        wavelength_range = (430, 760)
        illuminant = get_illuminant_in_range(D65_360_830_1NM, wavelength_range)

        self.assertIsNone(illuminant.get(360))
        self.assertIsNone(illuminant.get(830))

        sorted_keys = sorted(illuminant.keys())
        self.assertEquals((sorted_keys[0], sorted_keys[-1]), wavelength_range)

        self.assertEquals(D65_360_830_1NM[430], illuminant[430])
        self.assertEquals(D65_360_830_1NM[760], illuminant[760])

    def test_get_illuminant_in_range_when_provided_range_is_bigger(self):
        with self.assertRaises(RuntimeError):
            get_illuminant_in_range(D65_360_830_1NM, (430, 831))

    def test_get_illuminant_in_range_when_provided_range_is_smaller(self):
        with self.assertRaises(RuntimeError):
            get_illuminant_in_range(D65_360_830_1NM, (350, 830))

    def test_get_well_known_illuminant(self):
        wavelength_range = (430, 760)
        illuminant = get_well_known_illuminant('d65', wavelength_range)
        self.assertEquals(D65_360_830_1NM[430], illuminant[430])
        self.assertEquals(D65_360_830_1NM[760], illuminant[760])

    def test_get_well_known_illuminant_with_unknown_name(self):
        with self.assertRaises(RuntimeError):
            get_well_known_illuminant('unknown', (430, 760))

    def test_get_well_known_illuminant_with_bigger_range(self):
        with self.assertRaises(RuntimeError):
            get_well_known_illuminant('d65', (430, 831))

    def test_get_well_known_illuminant_with_smaller_range(self):
        with self.assertRaises(RuntimeError):
            get_well_known_illuminant('d65', (350, 830))

    def test_get_well_known_illuminant_identity(self):
        illuminant = get_well_known_illuminant('identity', (0, 900))
        self.assertListEqual([1] * 901, list(illuminant.values()))

    def test_get_illuminant_from_file(self):
        illuminant = get_illuminant_from_file(_ILLUMINANT_FILENAME)
        self.assertEqual(D65_360_830_1NM, illuminant)


if __name__ == '__main__':
    unittest.main()
