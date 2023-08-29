# Sentinel-Toolkit

# Description

This repository provides various utility tools for working with Sentinel data like:

1. Converting raw band dn values to sentinel responses.
2. Wrapper classes around a Sentinel-2 Product and Metadata.
3. Generating SQLite database for a given Ecostress Spectral Library.
4. Wrapper class around spectral.EcostressDatabase for querying with specific filters.
5. Wrapper class around Sentinel-2 Spectral Response Functions Excel file.
6. Converting a spectral distribution to Sentinel Responses.
7. Converting Ecostress Spectral Library to Sentinel Responses CSV file.

# Installation

Sentinel-Toolkit and its primary dependencies can be easily installed from the Python Package Index by issuing this
command in a shell:

```shell
$ pip install --user sentinel-toolkit
```

# Examples

## Converting Sentinel-2 DN values to Sentinel Responses

The new conversion formula for products after 25 January 2022 is integrated.

For more info
check https://forum.step.esa.int/t/changes-in-band-data-after-25-jan-2022-baseline-04-00-harmonizevalues-sentinel-2-l2a-snappy/36270

```python
from sentinel_toolkit.colorimetry import dn_to_sentinel

# The raw band(s) data
# For example: with 3 bands, 10980 x 10980 x 3 ndarray can be passed
bands_dn = None

# These values can be retrieved from product.S2ProductMetadata
# and this algorithm can be run easier from an S2Product object.
# See section "Working with Sentinel-2 Product".
nodata_value = 0
bands_offsets = [-1000, -1000, -1000]
quantification_value = 10000
normalized_solar_irradiances = [1, 0.9312, 0.7719]

sentinel_responses = dn_to_sentinel(bands_dn,
                                    nodata_value,
                                    bands_offsets,
                                    quantification_value,
                                    normalized_solar_irradiances)
```

## Working with Sentinel-2 Product and Metadata

### Working with Sentinel-2 Product Metadata

```python
from sentinel_toolkit.product import S2ProductMetadata

product_metadata = S2ProductMetadata("<path-to-metadata-filename>")

# With S2ProductMetadata you can retrieve:
# sensing data, nodata value, quantification value, band offsets
# and solar irradiances. Currently, these methods read directly
# from the xml and there is no caching.
product_metadata.get_sensing_date()
product_metadata.get_nodata_value()
product_metadata.get_quantification_value()
product_metadata.get_band_id_to_offset()
product_metadata.get_band_id_to_solar_irradiance()

band_ids = [1, 2, 3]
product_metadata.get_offsets(band_ids)
product_metadata.get_solar_irradiances(band_ids)
product_metadata.get_normalized_solar_irradiances(band_ids)
```

### Working with Sentinel-2 Product

```python
from sentinel_toolkit.product import S2Product

product = S2Product("<path-to-product-directory>")

product.get_directory_name()
product.get_metadata()

# If multiple sources are available for a given band
# for example B02_10m.jp2, B02_20m.jp2, B02_60m.jp2,
# the file with the best resolution will be selected.
# In the example case, this is B02_10m.jp2.
# (Currently this is implemented based on the band suffix).
product.get_dn_source(band_id=1)

band_ids = [1, 2, 3]
product.get_band_id_to_dn_source(band_ids)

# Converts the given bands to sentinel responses by
# using colorimetry.dn_to_sentinel() passing the required
# metadata arguments, so you don't have to do it yourself.
out_shape = (10980, 10980)
profile, sentinel_responses = product.dn_to_sentinel(band_ids, out_shape)
```

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

Given an Excel file containing the Sentinel-2 Spectral Response Functions, retrieve the wavelengths, band names and
bands_responses as colour.MultiSpectralDistributions and 2D ndarray:

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
from sentinel_toolkit.colorimetry.illuminants import D65_360_830_1NM

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

# You need to provide an illuminant, that at least covers the range of all the spectral distributions
# i.e. if your data contains values in (360, 830), then the illuminant should be in range (<= 360, >= 830)
# Otherwise, exception will be raised (currently no interpolation is performed on the illuminant)
illuminant = D65_360_830_1NM

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
$ python converter.py -e ecostress.db -s2 S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0.xlsx -s A -b 1 2 3 -ws 360 -we 830 -i d65
```
