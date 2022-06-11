"""
Srf
================

Srf module provides useful tools for working wth the Sentinel-2 Spectral Response Functions.
S2Srf class acs as a python wrapper around a given S2_SRF Excel file - it provides methods
for getting the wavelengths, band data, loading the whole data into
a colour.MultiSpectralDistributions object, etc.
"""

from .s2_srf import S2Srf
