"""This module contains functions to download us covid 19 data
on states/county/zip code level."""

import logging
import os
import json
import pandas as pd
import requests
import pickle

logger = logging.getLogger(__name__)
NYT_DATA = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'

current_dir = os.path.dirname(__file__)
abbrev_file_name = os.path.join(current_dir, 'asset/us_state_abbrev.json')
us_state_abbrev = json.load(open(abbrev_file_name))


def download_by_state(states, dates, columns=None):
    """
    :param dates: a string or a list of string to indicate the dates
    :param states: the two-letter state shorthand
    :param columns: there are a few columns in the original api, such as
    'date', 'state', 'positive', 'positiveIncrease', 'death', 'deathIncrease', and user
    can pick a subset of them
    :return: a dataframe with date and the positive and death cases for each day
    """

    if isinstance(dates, str):
        dates = [dates]

    if isinstance(states, str):
        states = [states]

    result = []

    for state in states:
        template = f'https://api.covidtracking.com/v1/states/{state}/daily.csv'
        rows = []
        header = []
        content = requests.get(template).text.split('\n')

        for idx, entry in enumerate(content):
            if idx != 0:
                rows.append(entry.split(','))
            else:
                header.extend(entry.split(','))

        covid_df = pd.DataFrame(rows, columns=header)
        covid_df['date'] = pd.to_datetime(covid_df['date'])

        if not columns:
            columns = ['date', 'state',
                       'positive', 'positiveIncrease',
                       'death', 'deathIncrease']
        else:
            # state and date must be in the columns
            # since they are the key
            for col in ['date', 'state']:
                if col not in columns:
                    columns.append(col)

        covid_df = covid_df[columns]
        result.append(covid_df)

    covid_df = pd.concat(result)
    # make the naming of columns to be consistent
    covid_df.rename({'positive': 'cases_cumulative',
                     'positiveIncrease': 'cases',
                     'death': 'deaths_cumulative',
                     'deathIncrease': 'deaths'}, axis=1, inplace=True)
    covid_df.dropna(subset=['date'], inplace=True)
    covid_df = covid_df[covid_df['date'].isin(dates)]
    covid_df.reset_index(drop=True, inplace=True)
    return covid_df


def download_by_county(counties, states, dates):
    """
    get the covid cases and deaths based on the new york times data base

    :param counties: name of the county (string), for example, Richland
    :param states: two-letter shorthand for state
    :param dates:
    :return: a dataframe with covid cases and deaths for given days and counties

    note that both a list or a string would work for most cases
    """
    counties = [counties] if isinstance(counties, str) else counties
    dates = [dates] if isinstance(dates, str) else dates
    states = [states] if isinstance(states, str) else states

    covid_df = download_county_level_data()
    if states:
        covid_df = covid_df[covid_df['state'].isin(states)]
    if counties:
        covid_df = covid_df[covid_df['county'].isin(counties)]
    if dates is not None:  # dates might be a pd.series
        covid_df = covid_df[covid_df['date'].isin(dates)]
    return covid_df


def download_by_zip_code(zip_code_list=None, dates=None):
    """
    get covid cases count based on zip code and dates
    :param zip_code_list: list or string of zip code
    :param dates: list or string of states
    :return: a dataframe of covid cases for given zip code and dates
    """
    logger.warning('the data are covid cases in the county where '
                   'the zip code belongs to in other words, different '
                   'zip code in the same county would return the same value')

    output_df = download_county_level_data()

    if isinstance(zip_code_list, str):
        zip_code_list = [zip_code_list]

    if isinstance(dates, str):
        dates = [dates]

    lookup_table = get_roll_up_county(rollup_from='zip')
    fips_list = []
    for zip_code in zip_code_list:
        try:
            state, county, fips_code, city_name = lookup_table[zip_code]
            fips_list.append(fips_code)
        except KeyError:
            logger.warning(f'cannot reverse lookup the zipcode {zip_code}')
            logger.warning(f'skipping')

    output_df = output_df[output_df['fips'].isin(fips_list)]
    output_df = output_df[output_df['date'].isin(pd.to_datetime(dates))]
    return output_df


def get_roll_up_county(rollup_from='zip'):
    """
    the most granular data is on country level,
    however, we also implemented zip code and city operation
    in this case, we will look up which county that city/zip belongs to.
    """
    try:
        data_file_dir = os.path.join(current_dir, f'{rollup_from}s_to_fips.pkl')
        with open(data_file_dir, 'rb') as f:
            lookup_dict = pickle.load(f)
        return lookup_dict

    except Exception:
        logger.warning('we need to compile the fips to zip lookup table,'
                       ' and this might take a while')
        # this pickle way only works for >= python3.8
        # fall back to parsing from scratch
        df_zips_and_fips = pd.read_csv(os.path.join(current_dir, 'asset/fips_and_zip.txt'),
                                       skiprows=1,
                                       dtype={'FIPS state': str,
                                              'State Postal Code': str,
                                              'county': str,
                                              'ZIP Census Tabulation Area': str})
        df_zips_and_fips = df_zips_and_fips[['State Postal Code',
                                             'county',
                                             'ZIP Census Tabulation Area',
                                             'cntyname',
                                             'zipname']]
        df_zips_and_fips.columns = ['state', 'fip', 'zip', 'county', 'city']
        lookup_dict = {}
        for _, row in df_zips_and_fips.iterrows():
            lookup_dict[row[rollup_from]] = (row['state'],
                                             row['county'],
                                             row['fip'],
                                             row['city']
                                             )
        return lookup_dict


def download_county_level_data():
    """
    download the original data by county
    this dataset will be further sliced as user request it
    """
    rows = []
    header = []
    content = requests.get(NYT_DATA).text.split('\n')
    for idx, entry_ in enumerate(content):
        if idx != 0:
            row = entry_.split(',')
            rows.append(row)
        else:
            header.extend(entry_.split(','))

    covid_df = pd.DataFrame(rows, columns=header)
    covid_df['state'] = covid_df['state'].apply(lambda x: us_state_abbrev[x])
    covid_df['cases'] = pd.to_numeric(covid_df['cases'])
    covid_df['deaths'] = pd.to_numeric(covid_df['deaths'])
    covid_df['date'] = pd.to_datetime(covid_df['date'])

    def get_daily(df_chunk):
        df_chunk = df_chunk[['date', 'deaths', 'cases']]
        df_with_date = df_chunk.set_index(['date'])
        df_with_date[['deaths_incremental', 'cases_incremental']] = df_with_date.diff()
        return df_with_date

    covid_df = covid_df.groupby(['county', 'state', 'fips']).apply(get_daily).reset_index()
    covid_df.dropna(subset=['deaths_incremental', 'cases_incremental'], inplace=True)
    covid_df.rename({'deaths': 'deaths_cumulative',
                     'cases': 'cases_cumulative',
                     'deaths_incremental': 'deaths',
                     'cases_incremental': 'cases'}, axis=1, inplace=True)
    covid_df.reset_index(drop=True, inplace=True)
    return covid_df
