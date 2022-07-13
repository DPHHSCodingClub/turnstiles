#!/usr/bin/env python
"""
mta is a library of functions for processing MTA turnstile data, available
at: http://web.mta.info/developers/turnstile.html
"""

from __future__ import division, print_function

import numpy as np
import pandas as pd


def read_csv(fname, verbose=False):
    """
    Take a raw MTA csv file and load into a cleaned pandas dataframe, ready
    for interactive usage.

    Input: filename of MTA turnstile data in CSV format, most recent spec (post
        2014).
    Output: pandas dataframe, with various keys and columns cleaned up,
        formatted, etc
    """
    df = pd.read_csv(fname)

    # remove any leading or trailing whitespace from key names
    for k in df.keys():
        if k.strip() != k:
            if verbose:
                print("strip whitespace from key {:s}".format(k.strip()))
            df = df.rename(columns={k: k.strip()})

    # merge date, time columns into a single datetime object
    # remain timezone naive; don't fuss about daylight savings
    # I have not yet deduced the turnstile timezone anyways...
    dt = df['DATE'] + " " + df['TIME']
    dt = pd.to_datetime(dt, format="%m/%d/%Y %H:%M:%S")
    del df['DATE']
    df['TIME'] = dt

    return df


# general idea: data is the fount of all truth
#   station = subset of dataframe w/ info for one station
#   turnstile = subset of dataframe w/ info for one turnstile


def select_station(df, station=None, linename=None, division=None):
    """
    Given processed dataframe, use some combination of STATION, LINENAME, or
    DIVISION to extract the data corresponding to one station, as desired by
    the user.
    """
    sels = []
    if station is not None:
        sels.append(df['STATION'] == station)
    if linename is not None:
        sels.append(df['LINENAME'] == linename)
    if division is not None:
        sels.append(df['DIVISION'] == division)

    # at least one selector must be provided
    assert len(sels) > 0

    selall = np.logical_and.reduce(sels)
    return df[selall]


def split_turnstiles(df):
    """
    Given data for a station, return a list of all the distinct turnstiles
    associated with that station.
    Input:
        pandas dataframe
    Output:
        list of pandas dataframes
    """
    x = []
    # obtain all the unique (C/A, UNIT, SCP) tuples
    # which correspond to individual turnstiles within a given station
    for k in df.groupby(['C/A', 'UNIT', 'SCP']).groups.keys():
        sels = [
            df['C/A']  == k[0],
            df['UNIT'] == k[1],
            df['SCP']  == k[2],
        ]
        selall = np.logical_and.reduce(sels)
        x.append(df[selall])
    return x


def is_turnstile_nominal(df):
    """
    Given entry/exit data for one turnstile, is the data clean and showing
    nominal behavior, namely...

    - entries and exits monotonically increase during the full time series
    - all "DESC" entries are "REGULAR", no instances of "RECOVR AUD"

    Input:
        pandas dataframe
    Output:
        teturns True if nominal, False otherwise.
    """
    return (
        np.all(df['DESC'] == 'REGULAR')
        and np.all(np.diff(df['ENTRIES']) >= 0)
        and np.all(np.diff(df['EXITS']) >= 0)
    )


def merge_dfs(ts_list):
    """
    Combine the entry and exit data for any list of dataframes (could be
    different stations, different turnstiles, etc...).

    All dataframes must have identical TIME column values.

    Input:
        list of pandas dataframes
    Output:
        pandas dataframe
    """
    merge = ts_list[0].copy(deep=True)  # not sure if deep copy is needed, so just in case
    merge = merge.reset_index(drop=True)

    # these keys only have meaning for individual stations
    del merge['STATION']
    del merge['LINENAME']
    del merge['DIVISION']
    # these keys only have meaning for individual turnstiles
    del merge['C/A']
    del merge['UNIT']
    del merge['SCP']
    del merge['DESC']

    for ts in ts_list[1:]:
        # must reset row indices to do pandas comparisons
        ts = ts.reset_index(drop=True)
        assert ts['TIME'].equals(merge['TIME'])
        merge['ENTRIES'] += ts['ENTRIES']
        merge['EXITS'] += ts['EXITS']

    return merge


if __name__ == '__main__':
    pass
