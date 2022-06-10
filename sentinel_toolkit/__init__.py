"""
Sentinel-Toolkit
================

`Sentinel-Toolkit <https://github.com/sentinel-toolkit/sentinel-toolkit>`__ is an open-source
`Python <https://www.python.org/>`__ package providing various utility tools for working
with Sentinel-2 satellite images. For example, you can use sentinel_toolkit.S2Srf class
as a python wrapper of a given S2_SRF Excel file to read the spectral responses into ndarray.
"""

from .s2_srf import S2Srf
