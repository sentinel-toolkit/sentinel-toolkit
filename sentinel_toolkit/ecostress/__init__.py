"""
Ecostress
================

Ecostress module provides tools for working with NASA Ecostress library.

It utilizes the library `spectral` and provides a script for loading the
Ecostress spectral data directory into an SQLite database.

It also provides the class Ecostress that adds some convenient methods
for working with spectral.EcostressDatabase
"""

from sentinel_toolkit.ecostress.ecostress_db_generator import generate_ecostress_db
from sentinel_toolkit.ecostress.ecostress import Ecostress
