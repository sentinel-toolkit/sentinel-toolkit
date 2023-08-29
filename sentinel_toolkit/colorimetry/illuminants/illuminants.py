"""
illuminants contains popular illuminant names to their 360_830 distributions as well as some
functions for reading and trimming illuminant distributions.
"""
import numpy as np

from sentinel_toolkit.colorimetry.illuminants.d65 import D65_360_830_1NM


def _generate_identity_illuminant(wavelength_range=(360, 830)):
    return {wl: 1.0 for wl in range(wavelength_range[0], wavelength_range[1] + 1)}


WELL_KNOWN_ILLUMINANTS = {
    'd65': D65_360_830_1NM,
    'identity': _generate_identity_illuminant()
}


def get_well_known_illuminant_names():
    """
    Retrieves the well known illuminant names.

    Returns
    -------
    out: list
        List of well known illuminant names
    """
    return set(WELL_KNOWN_ILLUMINANTS.keys())


def get_well_known_illuminant(illuminant_name, wavelength_range=(360, 830)):
    """
    Retrieves the illuminant distribution from ILLUMINANT_TO_DISTRIBUTION_MAPPINGS.
    Parameters
    ----------
    illuminant_name : str
        The name of the illuminant.
    wavelength_range : tuple of int
        The wavelength range.

    Returns
    -------
    output : dict
        The illuminant distribution.
    """
    if illuminant_name not in WELL_KNOWN_ILLUMINANTS:
        error_msg = f'The provided illuminant name "{illuminant_name}" is not supported! ' \
                    f'Supported illuminats: {get_well_known_illuminant_names()}'
        raise RuntimeError(error_msg)

    illuminant = WELL_KNOWN_ILLUMINANTS.get(illuminant_name)
    if illuminant_name == 'identity':
        # Here we can set 1s for all values in the range
        return _generate_identity_illuminant(wavelength_range)

    return get_illuminant_in_range(illuminant, wavelength_range)


def get_illuminant_from_file(illuminant_filename, wavelength_range=(360, 830)):
    """
    Retrieves the illuminant distribution from a file.
    Parameters
    ----------
    illuminant_filename : str
        The name of the file that contains the illuminant distribution.
    wavelength_range : tuple of int
        The wavelength range.

    Returns
    -------
    output : dict
        The illuminant distribution.
    """
    illuminant = _illuminant_file_to_dict(illuminant_filename)
    return get_illuminant_in_range(illuminant, wavelength_range)


def _illuminant_file_to_dict(illuminant_filename):
    result = {}
    with open(illuminant_filename, 'rb') as file:
        for line in file:
            (key, val) = line.split()
            result[int(key)] = np.float64(val)
    return result


def get_illuminant_in_range(illuminant, wavelength_range=(360, 830)):
    """
    Retrieves the illuminant values in a specific range.
    Parameters
    ----------
    illuminant : dict
        The illuminant distribution.
    wavelength_range : tuple of int
        The wavelength range.

    Returns
    -------
    output : dict
        The filtered illuminant distribution.
    """
    result = {wl: illuminant[wl] for wl in illuminant.keys() if
              _is_in_range(wl, wavelength_range)}

    if _failed_to_trim(result, wavelength_range):
        error_msg = f'The illuminant cannot be trimmed to {wavelength_range}.'
        raise RuntimeError(error_msg)

    return result


def _is_in_range(wavelength, wavelength_range):
    return wavelength_range[0] <= wavelength <= wavelength_range[1]


def _failed_to_trim(trim_result, wavelength_range):
    return len(trim_result) != wavelength_range[1] - wavelength_range[0] + 1
