import re
import logging


def unit_splitter(number):
    """
    When given a string, separate the numbers from their suffix's
    """
    unit = re.search('([A-Za-z]+)|(%)', number)  # Check for units or %
    if (number == '--') or (number == ''):  # For empty fields set number to None
        return [None, '']
    elif unit:  # If units are found
        reg = re.compile(unit.group())  # Create regex to search unit
        return unit_to_number(re.sub(reg, '', number), unit.group())  # Call function to convert units
    else:  # For numbers with no units
        return [float(number), '']


def unit_to_number(number, unit):
    """
    Convert units such as Million and Billion to their base form (eg 2M -> 2000000)
    """
    unit_dict = {
        'T': 1000000000000,
        'B': 1000000000,
        'M': 1000000,
        'K': 1000
    }

    if unit in unit_dict:  # If the units matches one of our units convert it to base form and remove unit.
        return [round(float(number) * unit_dict[unit]), '']
    elif unit == "%":
        return [float(number), unit]
    else:
        logging.warning("Unknown unit in unit_to_number()")
        raise ValueError("Unknown unit in unit_to_number()")
