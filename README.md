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
return a corresponding colour.MultiSpectralDistributions object:
```python
from sentinel_toolkit import read_s2_srf

s2a_srf = read_s2_srf("srf.xlsx", satellite="A", shape=(360, 830))
```

### Converting SpectralDistribution to Sentinel-2 Responses
Given a colour.SpectralDistribution, Illuminant and Spectral Response Functions,
calculate the Sentinel-2 Responses. (WIP)
