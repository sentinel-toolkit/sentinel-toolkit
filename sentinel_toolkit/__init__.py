"""
Sentinel-Toolkit
================

`Sentinel-Toolkit <https://github.com/sentinel-toolkit/sentinel-toolkit>`__ is an open-source
`Python <https://www.python.org/>`__ package providing various utility tools for working
with Sentinel-2 satellite images. For example, you can read S2_SRF functions as a
cmf colour.MultiSpectralDistributions object, convert colour.SpectralDistribution to
Spectral Responses.
"""

from .s2_srf import read_s2_srf
