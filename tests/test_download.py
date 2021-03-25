import pandas as pd
from covid19_us.download import get_daily_data, get_daily_data_by_county, get_daily_data_by_zip_code


def test_get_daily_data_list():
    """
    when dates is a list, we will download for each day, but not the whole range
    """
    sc_xmas = get_daily_data('SC',
                             dates=['2020-12-31', '2021-02-21'])

    assert len(sc_xmas) == 2
    assert 'cases' in sc_xmas
    assert 'deaths' in sc_xmas


def test_get_daily_data_range():
    """
    user can pass a date-range object and all the records from 0101 to 0110 will
    be downloaded in this case.
    """
    sc_xmas = get_daily_data('SC',
                             dates=pd.date_range('2021-01-01', '2021-01-10'))
    assert len(sc_xmas) == 10
    assert 'cases' in sc_xmas
    assert 'deaths' in sc_xmas
    assert 'cases_cumulative' in sc_xmas
    assert 'deaths_cumulative' in sc_xmas


def test_get_daily_data_by_county():
    """
    test passing a county name
    """
    shelby_valentine = get_daily_data_by_county(counties='Shelby',
                                                states='TN',
                                                dates='2021-02-14')
    assert len(shelby_valentine) == 1
    assert 'cases' in shelby_valentine
    assert 'deaths' in shelby_valentine
    assert 'cases_cumulative' in shelby_valentine
    assert 'deaths_cumulative' in shelby_valentine


def test_get_daily_data_by_zip_code():
    """
    test passing a zip code
    """
    watertown_new_year = get_daily_data_by_zip_code(zip_codes='02472',
                                                    dates='2021-01-01')
    assert len(watertown_new_year) == 1
    assert watertown_new_year['cases_cumulative'].iloc[0] > 0


def test_get_daily_data_by_zip_code_list():
    """
    test passing a list of zip code
    """
    watertown_new_year = get_daily_data_by_zip_code(zip_codes=['02472', '38120'],
                                                    dates='2021-01-01')
    assert len(watertown_new_year) == 2
    assert watertown_new_year['cases_cumulative'].iloc[0] > 0

    assert 'cases' in watertown_new_year
    assert 'deaths' in watertown_new_year
    assert 'cases_cumulative' in watertown_new_year
    assert 'deaths_cumulative' in watertown_new_year
