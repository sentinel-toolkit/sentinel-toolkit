"""
Ecostress
================

Ecostress module provides useful tools for working with NASA's Ecostress library.
It builds on top of spectral library and provides a script for loading the Ecostress
spectral data directory into an SQLite database. It also provides the class
Ecostress that can adds some convenient methods on top of the spectral libray.
"""

from .ecostress_db_generator import generate_ecostress_db
from .ecostress import Ecostress
