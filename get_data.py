# PART I. Getting the data

# I.A Auxiliary functions
# Functions for time and date format

import datetime

def date_format(astring):
    '''Assumes astring is a string which denotes a date in YYYY-MM-DD format.
    Returns astring as a date object from the datetime package.
    '''
    temp = astring.split('-')

    return datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))

def time_format(astring):
    '''Assumes astring is a string which denotes time in HH:MM:SS.MS format.
    Returns astring as a time object from the datetime package.
    '''
    temp = astring.split(':')
    temp[2] = temp[2].split('.')

    return datetime.time(int(temp[0]), int(temp[1]), int(temp[2][0]), int(temp[2][1]))


# I.B Killings data

def get_killings_data(file, date_col, time_col):
    '''Assumes file is a string denoting the file path and name to be loaded; date_col and time_col are
    numeric inputs that address the location of date and time information in the original data. Date should
    be in YYYY-MM-DD format and time in HH:MM:SS.MS.
    Returns a list of lists of the following scheme: [match ID, killing player ID, victim player ID, date, time]
    '''
    killings = []

    for line in open(file, 'r'):
        temp = line.split()

        # To date format
        temp[date_col] = date_format(temp[date_col])

        # To time format
        temp[time_col] = time_format(temp[time_col])

        # Append to database
        killings.append(temp)

    return killings


# I.C Cheaters data

def get_cheaters_data(file, est_date, ban_date):
    '''Assumes file is a string denoting the file path and name to be loaded; est_date and ban_date are
    numeric inputs that address the location of date information for the estimated cheating and banned date for
    the cheater.
    Returns a dictionary where the key is the cheating player ID and the value is the following list:
    [estimated cheating date, date when player was banned].
    '''
    cheaters = {}

    for line in open(file, 'r'):
        temp = line.split()

        # To date format
        temp[est_date] = date_format(temp[est_date])
        temp[ban_date] = date_format(temp[ban_date])

        cheaters[temp[0]] = [temp[1], temp[2]]

    return cheaters
