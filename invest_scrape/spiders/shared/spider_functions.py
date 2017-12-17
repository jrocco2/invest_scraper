import re
import logging
from datetime import date, datetime, timedelta


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


def generate_dates(self, start_date, end_date):
    """
    Generates all the dates in a specified range

    :param start_date: starting date in this form: date(2011, 10, 10)
    :param end_date: ending date in this form: date(2011, 10, 12)
    :return: a list of dates that can be used to access website data
    """

    def perdelta(start, end, delta):
        curr = start
        while curr <= end:
            yield curr
            curr += delta

    dates = []
    for result in perdelta(start_date, end_date, timedelta(days=1)):
        dates.append(result)

    return dates

def form_data(self, dates):
    formdata = {
        'country[]': ['29', '25', '54', '145', '47', '34', '174', '163', '32', '70', '6', '27', '37', '122', '15',
                      '78',
                      '113', '107', '55', '24', '121', '59', '89', '72', '71', '22', '17', '51', '39', '93', '106',
                      '14', '48', '66', '33', '23', '10', '119', '35', '92', '102', '57', '94', '97', '68', '96',
                      '103',
                      '111', '42', '109', '188', '7', '139', '247', '105', '172', '21', '43', '20', '60', '87',
                      '44',
                      '193', '125', '45', '53', '38', '170', '100', '56', '80', '52', '238', '36', '90', '112',
                      '110',
                      '11', '26', '162', '9', '12', '46', '85', '41', '202', '63', '123', '61', '143', '4', '5',
                      '138',
                      '178', '84', '75'],
        'timeZone': '31',
        'timeFilter': 'timeRemain',
        'dateFrom': str(dates),
        'dateTo': str(dates),
        'submitFilters': '1',
        'limit_from': '0',
    }

    return formdata