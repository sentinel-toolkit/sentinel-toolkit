"""
Product
================

Product module provides tools for working with Sentinel-2 product data.


metadata provides the class ProductMetadata that has methods
for retrieving information like Sensing Date, NODATA Value,
Quantification Value, BOA Offset Values, Solar Irradiances


"""

from sentinel_toolkit.product.product import Product
from sentinel_toolkit.product.metadata import ProductMetadata
