"""
s2_metadata provides the class S2ProductMetadata that acts as a python wrapper
of the Sentinel-2 product metadata.
"""

from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np


class S2ProductMetadata:
    """
    Provides methods for reading Sentinel-2 product metadata.
    """

    _SENSING_DATE_TAG = "DATATAKE_SENSING_START"

    _SPECIAL_VALUES_TAG = "Special_Values"
    _SPECIAL_VALUE_TEXT_TAG = "SPECIAL_VALUE_TEXT"
    _SPECIAL_VALUE_INDEX_TAG = "SPECIAL_VALUE_INDEX"
    _NODATA_TEXT_VALUE = "NODATA"

    _BOA_QUANTIFICATION_VALUE_TAG = "BOA_QUANTIFICATION_VALUE"
    _BOA_OFFSET_VALUES_LIST_TAG = "BOA_ADD_OFFSET_VALUES_LIST"
    _BOA_OFFSET_TAG = "BOA_ADD_OFFSET"
    _BOA_OFFSET_BAND_ID_ATTRIBUTE = "band_id"

    _SOLAR_IRRADIANCE_TAG = "SOLAR_IRRADIANCE"
    _SOLAR_IRRADIANCE_BAND_ID_ATTRIBUTE = "bandId"

    def __init__(self, filename):
        self.filename = filename
        file = Path(filename)
        self.tree = ET.parse(file)

    def get_filename(self):
        """
        Retrieves the metadata filename.

        Returns
        -------
        output : str
            The metadata filename.
        """
        return self.filename

    def get_sensing_date(self):
        """
        Retrieves the sensing date.

        Returns
        -------
        output : str
            The sensing date in format yyyy-mm-dd.
        """
        raw_sensing_date = self.tree.find(f'.//{self._SENSING_DATE_TAG}')
        sensing_date = raw_sensing_date.text.split('T')[0]
        return sensing_date

    def get_nodata_value(self):
        """
        Retrieves the nodata value.

        Returns
        -------
        output : int
            The nodata value, usually 0.
        """
        nodata_element = self.tree.find(
            f'.//{self._SPECIAL_VALUES_TAG}'
            f'[{self._SPECIAL_VALUE_TEXT_TAG} = "{self._NODATA_TEXT_VALUE}"]'
            f'/{self._SPECIAL_VALUE_INDEX_TAG}')
        nodata_value = int(nodata_element.text)
        return nodata_value

    def get_quantification_value(self):
        """
        Retrieves the BOA Quantification Value.

        Returns
        -------
        output : int
            The BOA quantification value, usually 10000.
        """
        boa_quantification_value_element = self.tree.find(
            f'.//{self._BOA_QUANTIFICATION_VALUE_TAG}')
        boa_quantification_value = int(boa_quantification_value_element.text)
        return boa_quantification_value

    def get_band_id_to_offset(self):
        """
        Retrieves a dictionary of band ids to BOA Offsets.

        Returns
        -------
        output : dict
            A dictionary containing the band id to BOA Offset mappings.
        """
        band_id_to_boa_offset = {}

        for boa_add_offset_element in self.tree.iter(self._BOA_OFFSET_TAG):
            band_id = int(boa_add_offset_element.attrib[self._BOA_OFFSET_BAND_ID_ATTRIBUTE])
            band_offset = int(boa_add_offset_element.text)
            band_id_to_boa_offset[band_id] = band_offset

        return band_id_to_boa_offset

    def get_offsets(self, band_ids):
        """
        Retrieves the BOA Offsets for the given band ids.

        Parameters
        ----------
        band_ids : list of int
            the band ids.

        Returns
        -------
        output : ndarray
            An array of the bands' BOA offsets.

        """
        return np.array([self.get_band_id_to_offset()[band_id] for band_id in band_ids])

    def get_band_id_to_solar_irradiance(self):
        """
        Retrieves a dictionary of band ids to solar irradiances.

        Returns
        -------
        output : dict
            A dictionary containing the band id to solar irradiance mappings.
        """
        band_id_to_solar_irradiance = {}

        for solar_irradiance_element in self.tree.iter(self._SOLAR_IRRADIANCE_TAG):
            band_id = int(solar_irradiance_element.attrib[self._SOLAR_IRRADIANCE_BAND_ID_ATTRIBUTE])
            solar_irradiance_value = float(solar_irradiance_element.text)
            band_id_to_solar_irradiance[band_id] = solar_irradiance_value

        return band_id_to_solar_irradiance

    def get_solar_irradiances(self, band_ids):
        """
        Retrieves the solar irradiances for the given band ids.

        Parameters
        ----------
        band_ids : list of int
            the band ids.

        Returns
        -------
        output : ndarray
            An array of the bands' solar irradiances.
        """
        return np.array([self.get_band_id_to_solar_irradiance()[band_id] for band_id in band_ids])

    def get_normalized_solar_irradiances(self, band_ids):
        """
        Retrieves the normalized solar irradiances for the given band ids.

        Parameters
        ----------
        band_ids : list of int
            the band ids.

        Returns
        -------
        output : ndarray
            An array of the normalized bands' solar irradiances.
        """
        solar_irradiances = self.get_solar_irradiances(band_ids)
        solar_irradiances = solar_irradiances / np.max(solar_irradiances)
        return solar_irradiances
