import ast
import os
import unittest
from unittest.mock import patch, mock_open

import numpy as np
from colour import SpectralDistribution

from sentinel_toolkit.colorimetry import SpectralData
from sentinel_toolkit.colorimetry import get_well_known_illuminant
from sentinel_toolkit.converter import EcostressToSentinelConverter
from sentinel_toolkit.srf import (S2Srf, S2SrfOptions)


class TestConverter(unittest.TestCase):
    _DB_FILENAME = "ecostress.db"
    _ECOSTRESS_DATA_DIRECTORY = "ecospeclib-all"

    _SRF_FILENAME = os.path.join(
        os.path.dirname(__file__),
        "test_data",
        "s2a_srf.xlsx"
    )
    _S2_SRF = S2Srf(_SRF_FILENAME)

    _SPECTRAL_DISTRIBUTIONS = {
        1: SpectralDistribution(
            {
                438: 0.104,
                439: 0.1042,
                440: 0.1043,
                441: 0.1044,
                442: 0.1045,
                443: 0.1046
            }
        ),
        2: SpectralDistribution(
            {
                2130: 0.404,
                2131: 0.4042,
                2132: 0.4043,
                2133: 0.4044,
                2134: 0.4045,
                2135: 0.4046
            }
        ),
        3: SpectralDistribution(
            {
                438: 0.204,
                439: 0.2042,
                440: 0.2043,
                441: 0.2044,
                442: 0.2045,
                443: 0.2046
            }
        ),
    }

    _EXPECTED_BANDS_RESPONSES_LINES_NUMBERS = [
        [1, 0.10434188863740076, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4043392311061295],
        [3, 0.20434188863740077, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]

    _BAND_NAMES = ["S2A_SR_AV_B1",
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

    @patch('sentinel_toolkit.ecostress.Ecostress')
    @patch('builtins.open', new_callable=mock_open())
    def test_convert_ecostress_to_sentinel(self, mock_open_file, mock_ecostress):
        spectrum_ids = list(self._SPECTRAL_DISTRIBUTIONS.keys())
        mock_ecostress.get_spectrum_ids.return_value = spectrum_ids

        spectral_distributions = self._SPECTRAL_DISTRIBUTIONS.values()
        spectral_data_list = [SpectralData(sd.wavelengths, sd.values) for sd in spectral_distributions]
        mock_ecostress.get_spectral_distribution_numpy.side_effect = spectral_data_list

        converter = EcostressToSentinelConverter(mock_ecostress, self._S2_SRF)

        s2_srf_options = S2SrfOptions(wavelength_range=(360, 2600))
        illuminant = get_well_known_illuminant('identity', (360, 2600))
        converter.convert_ecostress_to_sentinel_csv(s2_srf_options, illuminant)

        mock_open_file.assert_called_once_with('sentinel_A.csv', 'w', encoding='utf-8')

        band_names_line = ','.join(self._BAND_NAMES)
        call_args = mock_open_file.return_value.__enter__().write.call_args_list

        header_line = call_args[0].args[0]
        self.assertEqual(f"SpectrumID,{band_names_line}\n", header_line)

        bands_responses_lines = [call_arg.args[0] for call_arg in call_args[1:]]
        lines_number_lists = [self._line_to_number_list(line) for line in bands_responses_lines]
        np.testing.assert_array_almost_equal(self._EXPECTED_BANDS_RESPONSES_LINES_NUMBERS, lines_number_lists)

    @staticmethod
    def _line_to_number_list(line):
        number_list = line.split(",")
        number_list = [ast.literal_eval(number) for number in number_list]
        return number_list


if __name__ == '__main__':
    unittest.main()
