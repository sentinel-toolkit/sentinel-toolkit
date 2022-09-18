"""
s2_product provides the class S2Product that provides various
tools for working with Sentinel-2 product data.
"""

import re
from pathlib import Path

import numpy as np
import rasterio

from rasterio.enums import Resampling

from sentinel_toolkit.colorimetry import dn_to_sentinel
from . import product_metadata


class S2Product:
    """
    Provides methods for working with a Sentinel-2 product.
    """

    _METADATA_FILENAME_REGEX = 'MTD_MSIL*.xml'
    _BAND_ID_TO_NAME = {
        0: 'B01',
        1: 'B02',
        2: 'B03',
        3: 'B04',
        4: 'B05',
        5: 'B06',
        6: 'B07',
        7: 'B08',
        8: 'B8A',
        9: 'B09',
        10: 'B10',
        11: 'B11',
        12: 'B12',
    }
    _R10M_FILE_REGEX = ".*10m.jp2"
    _R20M_FILE_REGEX = ".*20m.jp2"
    _R60M_FILE_REGEX = ".*60m.jp2"
    _JP2_DRIVER_NAME = "JP2OpenJPEG"
    _TIFF_DRIVER_NAME = "GTiff"

    def __init__(self, product_directory_name):
        self.directory_name = product_directory_name
        metadata_filename = self._get_metadata_filename()
        self.metadata = product_metadata.S2ProductMetadata(metadata_filename)

    def _get_metadata_filename(self):
        metadata_filenames = self._find_filenames(
            self._METADATA_FILENAME_REGEX,
            recursive=False
        )

        metadata_filenames_count = len(metadata_filenames)
        if metadata_filenames_count == 1:
            return metadata_filenames[0]

        raise RuntimeError(f'Number of found metadata files matching '
                           f'regex {self._METADATA_FILENAME_REGEX} '
                           f'is {metadata_filenames_count}.')

    def _find_filenames(self, regex, recursive=True):
        if recursive:
            file_paths = Path(self.directory_name).rglob(regex)
        else:
            file_paths = Path(self.directory_name).glob(regex)

        filenames = []
        for file_path in file_paths:
            filenames.append(str(file_path))

        return filenames

    def get_directory_name(self):
        """
        Retrieves the product directory name.

        Returns
        -------
        output : str
            The product directory name.
        """
        return self.directory_name

    def get_metadata(self):
        """
        Retrieves the metadata of the product.

        Returns
        -------
        output : sentinel_toolkit.product.metadata.metadata.S2ProductMetadata
            The metadata of the product.
        """
        return self.metadata

    def get_dn_source(self, band_id):
        """
        Retrieves the dn source.

        When multiple files with different Spatial Resolution
        are found, the best resolution is selected.

        Parameters
        ----------
        band_id : int
            The band id.

        Returns
        -------
        output : rasterio.io.DatasetReader
            A rasterio.io.DatasetReader object.
        """
        band_name = self._BAND_ID_TO_NAME[band_id]
        if band_name is None:
            raise RuntimeError(f"Unsupported band id {band_id}.")

        bands_filenames = self._find_filenames(f"*{band_name}*.jp2",
                                               recursive=True)
        if len(bands_filenames) == 0:
            raise RuntimeError(f"Number of found files for band id {band_id} "
                               f"with band name {band_name} is 0.")

        if len(bands_filenames) == 1:
            band_filename = bands_filenames[0]
        else:
            band_filename = self._get_best_band_filename(bands_filenames)
            if band_filename is None:
                raise RuntimeError(f"Cannot find a band file matching regex "
                                   f"{self._R10M_FILE_REGEX} or "
                                   f"{self._R20M_FILE_REGEX} or "
                                   f"{self._R60M_FILE_REGEX}.")

        band_source = rasterio.open(band_filename,
                                    driver=self._JP2_DRIVER_NAME)
        return band_source

    def _get_best_band_filename(self, bands_filenames):
        for band_filename in bands_filenames:
            if re.match(self._R10M_FILE_REGEX, band_filename):
                return band_filename

        for band_filename in bands_filenames:
            if re.match(self._R20M_FILE_REGEX, band_filename):
                return band_filename

        for band_filename in bands_filenames:
            if re.match(self._R60M_FILE_REGEX, band_filename):
                return band_filename

        return None

    def get_band_id_to_dn_source(self, band_ids):
        """
        Retrieves a dictionary of band ids to DN sources.

        Parameters
        ----------
        band_ids : list of int
            The band ids.

        Returns
        -------
        output : dict
            A dictionary containing the band id to DN source mappings.
        """
        band_id_to_dn = {}
        for band_id in band_ids:
            band_id_to_dn[band_id] = self.get_dn_source(band_id)
        return band_id_to_dn

    def dn_to_sentinel(self, band_ids, out_shape=(10980, 10980)):
        """
        Converts the product dn values to sentinel responses.

        Parameters
        ----------
        band_ids : list of int
            The band ids.

        out_shape : tuple of int
            The out shape.

        Returns
        -------
        output : tuple of rasterio.profiles.Profile and numpy.ndarray
            A tuple containing the modified rasterio profile (with the
            new out_shape and driver GTiff) and the sentinel responses.
        """
        band_id_to_dn_source = self.get_band_id_to_dn_source(band_ids)
        band_id_to_dn = {}

        for band_id, dn_source in band_id_to_dn_source.items():
            band_dn = dn_source.read(1, out_shape=out_shape, resampling=Resampling.cubic)
            band_id_to_dn[band_id] = band_dn

        bands_dn = [band_id_to_dn[band_id] for band_id in band_ids]
        raw_bands_data = np.stack(bands_dn, axis=-1).astype(np.float32)

        metadata = self.metadata
        sentinel_image = dn_to_sentinel(
            raw_bands_data,
            metadata.get_nodata_value(),
            metadata.get_offsets(band_ids),
            metadata.get_quantification_value(),
            metadata.get_normalized_solar_irradiances(band_ids)
        )

        profile = band_id_to_dn_source[band_ids[0]].profile
        self._update_profile(sentinel_image, profile)

        return profile, sentinel_image

    def _update_profile(self, image, profile):
        height, width, count = image.shape

        profile.update({
            'width': width,
            'height': height,
            'count': count,
            'dtype': rasterio.uint8,
            'driver': self._TIFF_DRIVER_NAME
        })
