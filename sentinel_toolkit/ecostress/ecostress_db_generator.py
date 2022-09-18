"""
ecostress_db_generator provides a way to generate SQLite database
containing the Ecostress spectral library.
ecostress_db_generator.py can be used as a script to generate
the database in the following manner:

python ecostress_db_generator.py -d <ecostress_directory> -o <output_filename>

"""

from argparse import ArgumentParser
from pathlib import Path
from spectral import EcostressDatabase

_DB_FILENAME = "ecostress.db"
_ECOSTRESS_DATA_DIRECTORY = "ecospeclib-all"


def generate_ecostress_db(ecostress_dir=_ECOSTRESS_DATA_DIRECTORY, output_db_filename=_DB_FILENAME):
    """
    Generates SQLite database for a given Ecostress spectral library directory.

    Parameters
    ----------
    ecostress_dir : str
        The Ecostress spectral library directory.
        If missing, default to "ecospeclib-all".
    output_db_filename : str
        The name of the output SQLite database file.
        If missing, default to "ecostress.db".
    """
    EcostressDatabase.create(output_db_filename, ecostress_dir)


def _main():
    args = _parse_args()
    ecostress_dir = args.dir
    output_db_filename = args.out

    ecostress_dir_path = Path(ecostress_dir)
    if not ecostress_dir_path.is_dir():
        error_msg = f'The provided ecostress data directory "{ecostress_dir}" does not exist!'
        raise RuntimeError(error_msg)

    generate_ecostress_db(ecostress_dir, output_db_filename)


def _parse_args():
    parser = ArgumentParser(description="Ecostress SQLite Database Generator")
    parser.add_argument('-d', '--dir', required=False, type=str, default=_ECOSTRESS_DATA_DIRECTORY,
                        help="Ecostress data directory")
    parser.add_argument('-o', '--out', required=False, type=str, default=_DB_FILENAME,
                        help="The filename that will be used to store the SQLite database")

    return parser.parse_args()


if __name__ == "__main__":
    _main()
