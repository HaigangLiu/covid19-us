import pandas as pd
from covid19_us import download_by_state, \
    download_by_county, download_by_zip_code


def test_download_by_state():
    """
    when dates is a list, we will download for each day, but not the whole range
    """
    date_list = download_by_state('SC', dates=['2020-12-31', '2021-02-21'])
    assert len(date_list) == 2
    assert 'cases' in date_list
    assert 'deaths' in date_list
    assert 'cases_cumulative' in date_list
    assert 'deaths_cumulative' in date_list

    single_day = download_by_state('SC', dates='2020-12-31')
    assert len(single_day) == 1
    assert 'cases' in single_day
    assert 'deaths' in single_day
    assert 'cases_cumulative' in single_day
    assert 'deaths_cumulative' in single_day

    date_range = download_by_state('SC', dates=pd.date_range('2021-01-01', '2021-01-10'))
    assert len(date_range) == 10
    assert 'cases' in date_range
    assert 'deaths' in date_range
    assert 'cases_cumulative' in date_range
    assert 'deaths_cumulative' in date_range

    multiple_states = download_by_state(states=['SC', 'NC'],
                                        dates=['2020-12-31', '2021-02-21'])
    assert len(multiple_states) == 4
    assert 'cases' in multiple_states
    assert 'deaths' in multiple_states
    assert 'cases_cumulative' in multiple_states
    assert 'deaths_cumulative' in multiple_states


def test_get_daily_data_by_county():
    """
    test passing a county name
    """
    shelby_valentine = download_by_county(counties='Shelby',
                                          states='TN',
                                          dates='2021-02-14')
    assert len(shelby_valentine) == 1
    assert 'cases' in shelby_valentine
    assert 'deaths' in shelby_valentine
    assert 'cases_cumulative' in shelby_valentine
    assert 'deaths_cumulative' in shelby_valentine

    shelby_two_days = download_by_county(counties='Shelby',
                                         states='TN',
                                         dates=['2021-02-14', '2021-01-01'])
    assert len(shelby_two_days) == 2
    assert 'cases' in shelby_two_days
    assert 'deaths' in shelby_two_days
    assert 'cases_cumulative' in shelby_two_days
    assert 'deaths_cumulative' in shelby_two_days

    shelby_multiple_days = download_by_county(counties='Shelby',
                                              states='TN',
                                              dates=pd.date_range('2020-10-31', '2020-11-07'))
    assert len(shelby_multiple_days) == 8
    assert 'cases' in shelby_multiple_days
    assert 'deaths' in shelby_multiple_days
    assert 'cases_cumulative' in shelby_multiple_days
    assert 'deaths_cumulative' in shelby_multiple_days

    two_counties = download_by_county(counties=['Shelby', 'Richland'],
                                      states=['TN', 'SC'],
                                      dates=pd.date_range('2020-10-31', '2020-11-01'))
    assert len(two_counties) == 4
    assert 'cases' in two_counties
    assert 'deaths' in two_counties
    assert 'cases_cumulative' in two_counties
    assert 'deaths_cumulative' in two_counties


def test_get_daily_data_by_zip_code():
    """
    test passing a zip code
    """
    watertown_new_year_one_zip = download_by_zip_code(zip_code_list='02472',
                                                      dates='2021-01-01')
    assert len(watertown_new_year_one_zip) == 1
    assert watertown_new_year_one_zip['cases_cumulative'].iloc[0] > 0

    watertown_new_year_two_zips = download_by_zip_code(zip_code_list=['02472', '38120'],
                                                       dates='2021-01-01')
    assert len(watertown_new_year_two_zips) == 2
    assert watertown_new_year_two_zips['cases_cumulative'].iloc[0] > 0

    assert 'cases' in watertown_new_year_two_zips
    assert 'deaths' in watertown_new_year_two_zips
    assert 'cases_cumulative' in watertown_new_year_two_zips
    assert 'deaths_cumulative' in watertown_new_year_two_zips

    multiple_zips = download_by_zip_code(zip_code_list=['02472', '38120'],
                                         dates='2021-01-01')
    assert len(multiple_zips) == 2
    assert multiple_zips['cases_cumulative'].iloc[0] > 0
    assert 'cases' in multiple_zips
    assert 'deaths' in multiple_zips
    assert 'cases_cumulative' in multiple_zips
    assert 'deaths_cumulative' in multiple_zips
