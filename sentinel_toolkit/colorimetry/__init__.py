"""
Colorimetry
================

Colorimetry module provides tools for converting dn values or
spectral distribution to sentinel.
"""

from sentinel_toolkit.colorimetry.sentinel_values import SpectralData

from sentinel_toolkit.colorimetry.sentinel_values import sd_to_sentinel_colour
from sentinel_toolkit.colorimetry.sentinel_values import sd_to_sentinel_direct_colour

from sentinel_toolkit.colorimetry.sentinel_values import sd_to_sentinel_numpy
from sentinel_toolkit.colorimetry.sentinel_values import sd_to_sentinel_direct_numpy

from sentinel_toolkit.colorimetry.sentinel_values import dn_to_sentinel

from sentinel_toolkit.colorimetry.illuminants import D65_360_830_1NM
from sentinel_toolkit.colorimetry.illuminants import WELL_KNOWN_ILLUMINANTS
from sentinel_toolkit.colorimetry.illuminants import get_well_known_illuminant
from sentinel_toolkit.colorimetry.illuminants import get_illuminant_from_file
from sentinel_toolkit.colorimetry.illuminants import get_illuminant_in_range
from sentinel_toolkit.colorimetry.illuminants import get_well_known_illuminant_names
