# Sentinel-Toolkit

## Description

This repository provides various utility tools for working with Sentinel data like:

1. Reading Sentinel-2 Spectral Response Functions
2. Converting colour.SpectralDistribution to Sentinel Responses

## Installation

Sentinel-Toolkit and its primary dependencies can be easily installed from the Python Package Index by issuing this
command in a shell:

```shell
$ pip install --user sentinel-toolkit
```

## Examples

### Reading Sentinel-2 Spectral Response Functions

Given an Excel file containing the Sentinel-2 Spectral Response Functions,
read Band2, Band3 and Band4 data in the wavelength range of (360, 830)
into a corresponding colour.MultiSpectralDistributions object:

```python
from sentinel_toolkit import S2Srf

s2a_srf = S2Srf("srf.xlsx", satellite="A")
bn = ["S2A_SR_AV_B2", "S2A_SR_AV_B3", "S2A_SR_AV_B4"]
wr = (360, 830)

bands_responses_distribution = s2a_srf.get_bands_responses_distribution(band_names=bn, wavelength_range=wr)
```

Given an Excel file containing the Sentinel-2 Spectral Response Functions,
read all band data in the wavelength range of (360, 830)
into a corresponding ndarray:

```python
from sentinel_toolkit import S2Srf

s2a_srf = S2Srf("srf.xlsx", satellite="A")

# By default, band_names is all band names and wavelength_range is (360, 830)
all_bands_responses = s2a_srf.get_bands_responses()
```

### Converting SpectralDistribution to Sentinel-2 Responses

Given a colour.SpectralDistribution, Illuminant and Spectral Response Functions,
calculate the Sentinel-2 Responses. (WIP)
