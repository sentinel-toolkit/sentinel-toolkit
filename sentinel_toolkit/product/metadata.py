from pathlib import Path
import xml.etree.ElementTree as ET


class ProductMetadata:
    _SENSING_DATE_TAG = "DATATAKE_SENSING_START"

    _SPECIAL_VALUES_TAG = "Special_Values"
    _SPECIAL_VALUE_TEXT_TAG = "SPECIAL_VALUE_TEXT"
    _SPECIAL_VALUE_INDEX_TAG = "SPECIAL_VALUE_INDEX"
    _NODATA_TEXT_VALUE = "NODATA"

    _BOA_QUANTIFICATION_VALUE_TAG = "BOA_QUANTIFICATION_VALUE"

    BAND_IDS_TO_NAMES = {
        0: 'B01',
        1: 'B02',
        2: 'B03',
        3: 'B04',
        4: 'B04',
        5: 'B04',
        6: 'B04',
        7: 'B04',
        8: 'B04',
    }

    def __init__(self, metadata_filename):
        metadata_file = Path(metadata_filename)
        self.metadata_xml_tree = ET.parse(metadata_file)

    def get_sensing_data(self):
        raw_sensing_date = self.metadata_xml_tree.find(self._SENSING_DATE_TAG)
        sensing_date = raw_sensing_date.text.split('T')[0]
        return sensing_date

    def get_nodata_value(self):
        nodata_element = self.metadata_xml_tree.find(
            f'./{self._SPECIAL_VALUES_TAG}[{self._SPECIAL_VALUE_TEXT_TAG} = "{self._NODATA_TEXT_VALUE}"]'
            f'/{self._SPECIAL_VALUE_INDEX_TAG}')
        nodata_value = nodata_element.text
        return nodata_value

    def get_boa_quantification_value(self):
        boa_quantification_value_element = self.metadata_xml_tree.find(self._BOA_QUANTIFICATION_VALUE_TAG)
        boa_quantification_value = int(boa_quantification_value_element.text)
        return boa_quantification_value

    def get_boa_add_offset_values_list(self, band_ids):
        pass

