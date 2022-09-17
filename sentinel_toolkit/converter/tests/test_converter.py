import unittest
from unittest import mock
from unittest.mock import patch, mock_open

import numpy as np
from colour import SpectralDistribution

from sentinel_toolkit.colorimetry.sentinel_values import SpectralData
from sentinel_toolkit.converter import EcostressToSentinelConverter


class TestConverter(unittest.TestCase):
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

    @patch('sentinel_toolkit.srf.S2Srf')
    @patch('sentinel_toolkit.ecostress.Ecostress')
    @patch('builtins.open', new_callable=mock_open())
    def test_dump(self, mock_open_file, mock_ecostress, mock_s2_srf):
        mock_s2_srf.get_band_names.return_value = self._BAND_NAMES
        mock_s2_srf.get_bands_responses.return_value = self._BANDS_RESPONSES

        mock_ecostress.get_spectrum_ids.return_value = np.array([1])
        spectral_data = SpectralData(self._SPECTRAL_DISTRIBUTION.wavelengths,
                                     self._SPECTRAL_DISTRIBUTION.values)
        mock_ecostress.get_spectral_distribution_numpy.return_value = spectral_data

        converter = EcostressToSentinelConverter(mock_ecostress, mock_s2_srf)
        converter.convert_ecostress_to_sentinel_csv()
        mock_open_file.assert_called_once_with('sentinel_A.csv', 'w', encoding='utf-8')

        band_names_line = ','.join(self._BAND_NAMES)
        csv_heading = f"SpectrumID,{band_names_line}\n"
        csv_sentinel_responses_line = \
            "1,10.985433231270072,11.086160373966965,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\n"

        mock_open_file.return_value.__enter__().write.assert_has_calls([
            mock.call(csv_heading),
            mock.call(csv_sentinel_responses_line)
        ])


if __name__ == '__main__':
    unittest.main()
