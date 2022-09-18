"""
Product
================

Product module provides tools for working with Sentinel-2 product data.


metadata provides the class ProductMetadata that has methods
for retrieving information like Sensing Date, NODATA Value,
Quantification Value, BOA Offset Values, Solar Irradiances

product provides the class Product that has methods for working with
band data - for example: read specific band, convert dn to sentinel,
get the metdata.

"""

from sentinel_toolkit.product.s2_product import Product
from sentinel_toolkit.product.s2_metadata import ProductMetadata
