"""
Srf
================

Srf module provides tools for working with the Sentinel-2 SRF.

S2Srf class acts as a python wrapper around a given S2_SRF Excel file.
It provides methods for getting the wavelengths, band data, loading the
whole data into a colour.MultiSpectralDistributions object, etc.

S2SrfOptions is a wrapper around the satellite, band names and wavelength
range properties.
"""

from sentinel_toolkit.srf.s2_srf import S2Srf
from sentinel_toolkit.srf.s2_srf import S2SrfOptions
