import unittest
from unittest.mock import patch

from sentinel_toolkit.ecostress import generate_ecostress_db


class TestEcostressDbGenerator(unittest.TestCase):
    _DB_FILENAME = "ecostress.db"
    _ECOSTRESS_DATA_DIRECTORY = "ecospeclib-all"

    @patch('spectral.EcostressDatabase.create')
    def test_generate_ecostress_db(self, mock_ecostress_database_create):
        generate_ecostress_db(self._ECOSTRESS_DATA_DIRECTORY, self._DB_FILENAME)
        mock_ecostress_database_create.assert_called_once_with(self._DB_FILENAME, self._ECOSTRESS_DATA_DIRECTORY)


if __name__ == '__main__':
    unittest.main()
