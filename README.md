# Sentinel-Toolkit

# Description

This repository provides various utility tools for working with Sentinel data like:

1. Generating of SQLite database for a given Ecostress Spectral Library.
2. Wrapper class around spectral.EcostressDatabase for querying with specific filters.
3. Wrapper class around Sentinel-2 Spectral Response Functions Excel file.
4. Converting a spectral distribution to Sentinel Responses.
5. Converting Ecostress Spectral Library to Sentinel Responses CSV file.

# Installation

Sentinel-Toolkit and its primary dependencies can be easily installed from the Python Package Index by issuing this
command in a shell:

```shell
$ pip install --user sentinel-toolkit
```

# Examples

## Loading and working with Ecostress Spectral Library

### Generating SQLite database

Generate the SQLite database given the Ecostress spectral library directory:

```python
from sentinel_toolkit.ecostress import generate_ecostress_db

generate_ecostress_db("ecospeclib-all", "ecostress.db")
```

For convenience, there is a main method in ecostress_db_generator.py that can be called from shell like so:

```shell
$ python ecostress_db_generator.py -d /ecospeclib-all -o ecostress.db
```

### Working with the generated SQLite database

```python
from spectral import EcostressDatabase
from sentinel_toolkit.ecostress import Ecostress

ecostress_db = EcostressDatabase("ecostress.db")
ecostress = Ecostress(ecostress_db)

# Get all the spectrum ids that contain some values in the given range (420, 830).
wavelength_range = (420, 830)
spectrum_ids = ecostress.get_spectrum_ids(wavelength_range)

# Iterate over the found spectrum_ids and get colour.SpectralDistribution objects.
spectral_distributions_colour = []
for spectrum_id in spectrum_ids:
    spectral_distribution = ecostress.get_spectral_distribution_colour(spectrum_id)
    spectral_distributions_colour.append(spectral_distribution)

# Iterate over the found spectrum_ids and get numpy arrays.
# This can be used for gaining better performance
spectral_distributions_numpy = []
for spectrum_id in spectrum_ids:
    spectral_distribution = ecostress.get_spectral_distribution_numpy(spectrum_id)
    spectral_distributions_numpy.append(spectral_distribution)
```

## Reading Sentinel-2 Spectral Response Functions

Given an Excel file containing the Sentinel-2 Spectral Response Functions,
retrieve the wavelengths, band names and bands_responses as colour.MultiSpectralDistributions
and 2D ndarray:

```python
from sentinel_toolkit.srf import S2Srf, S2SrfOptions

s2a_srf = S2Srf("srf.xlsx")

# Retrieve the wavelengths of Sentinel-2A as ndarray.
wavelengths = s2a_srf.get_wavelengths()

# Retrieve all the band names of Sentinel-2A bands 1, 2 and 3 as ndarray.
band_names = s2a_srf.get_band_names(band_ids=[1, 2, 3])

# Retrieve B2, B3, B4 of Sentinel-2A satellite in wavelength range (360, 830)
# as colour.MultiSpectralDistributions.
satellite = 'A'
band_ids_option = [1, 2, 3]
wavelength_range = (360, 830)
s2_srf_options = S2SrfOptions(satellite, band_ids_option, wavelength_range)
bands_responses_distribution = s2a_srf.get_bands_responses_distribution(s2_srf_options)

# Retrieve all bands responses of Sentinel-2B in wavelength range (360, 830) as 2D ndarray.
satellite = 'B'
wavelength_range = (360, 830)
s2_srf_options = S2SrfOptions(satellite=satellite, wavelength_range=wavelength_range)
bands_responses = s2a_srf.get_bands_responses(s2_srf_options)
```

## Converting SpectralDistribution to Sentinel-2 Responses

Convert a spectral distribution to Sentinel-2 Responses:

```python
from spectral import EcostressDatabase
from sentinel_toolkit.ecostress import Ecostress
from sentinel_toolkit.srf import S2Srf, S2SrfOptions
from sentinel_toolkit.colorimetry import sd_to_sentinel_numpy, sd_to_sentinel_direct_numpy
from sentinel_toolkit.colorimetry.illuminants import D65_360_830_1NM_VALUES

ecostress_db = EcostressDatabase("ecostress.db")
ecostress = Ecostress(ecostress_db)
s2a_srf = S2Srf("srf.xlsx")

wavelength_range = (360, 830)

spectrum_id = 1
# Use the numpy version for better performance
spectral_data = ecostress.get_spectral_distribution_numpy(spectrum_id, wavelength_range)

spectral_data_min_wavelength = spectral_data.wavelengths[0]
spectral_data_max_wavelength = spectral_data.wavelengths[-1]

wr_start = max(wavelength_range[0], spectral_data_min_wavelength)
wr_end = min(wavelength_range[1], spectral_data_max_wavelength)

# Reshape the illuminant to the spectral distribution shape
illuminant = D65_360_830_1NM_VALUES[wr_start - 360: wr_end - 359]

# Get the sentinel responses for spectrum with id 1 for all bands
# from satellite 'A' in wavelength_range (360, 830)
s2_srf_options = S2SrfOptions(satellite='A', wavelength_range=(wr_start, wr_end))
sentinel_responses = sd_to_sentinel_numpy(spectral_data,
                                          s2a_srf,
                                          s2_srf_options,
                                          illuminant)

# Another way of doing this would be:
s2_srf_options = S2SrfOptions(satellite='A', wavelength_range=(wr_start, wr_end))
bands_responses = s2a_srf.get_bands_responses(s2_srf_options)
sentinel_responses = sd_to_sentinel_direct_numpy(spectral_data, bands_responses, illuminant)
```

## Converting full Ecostress Spectral Library to Sentinel-2 Responses CSV file

Generate a CSV file containing the Sentinel-2 responses for all materials from the Ecostress library:

```python
from spectral import EcostressDatabase
from sentinel_toolkit.ecostress import Ecostress
from sentinel_toolkit.srf import S2Srf
from sentinel_toolkit.converter import EcostressToSentinelConverter

ecostress_db = EcostressDatabase("ecostress.db")
ecostress = Ecostress(ecostress_db)

s2a_srf = S2Srf("srf.xlsx")

converter = EcostressToSentinelConverter(ecostress, s2a_srf)
converter.convert_ecostress_to_sentinel_csv()
```

For convenience, there is a main method in converter.py that can be called from shell like so:

```shell
$ python converter.py -e ecostress.db -s2 S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0.xlsx -s A -b 1 2 3 -ws 360 -we 830
```
