import pandas as pd
from covid19_us import download


def test_get_daily_data_list():
    """
    when dates is a list, we will download for each day, but not the whole range
    """
    sc_xmas = download.get_daily_data('SC',
                                      dates=['2020-12-31', '2021-02-21'],
                                      columns=['positiveIncrease'])
    assert len(sc_xmas) == 2
    assert 'positiveIncrease' in sc_xmas
    assert 'death' not in sc_xmas


def test_get_daily_data_range():
    """
    user can pass a date-range object and all the records from 0101 to 0110 will
    be downloaded in this case.
    """
    sc_xmas = download.get_daily_data('SC',
                                      dates=pd.date_range('2021-01-01', '2021-01-10'),
                                      columns=['positiveIncrease'])
    assert len(sc_xmas) == 10
    assert 'positiveIncrease' in sc_xmas
    assert 'death' not in sc_xmas


def test_get_daily_data_by_county():
    """
    test passing a county name
    """
    shelby_valentine = download.get_daily_data_by_county(counties='Shelby',
                                                         states='TN',
                                                         dates='2021-02-14')
    assert len(shelby_valentine) == 1


def test_get_daily_data_by_zip_code():
    """
    test passing a zip code
    """
    watertown_new_year = download.get_daily_data_by_zip_code(zip_codes='02472',
                                                             dates='2021-01-01')
    assert len(watertown_new_year) == 1
    assert watertown_new_year['cases'].iloc[0] > 0


def test_get_daily_data_by_zip_code():
    """
    test passing a list of zip code
    """
    watertown_new_year = download.get_daily_data_by_zip_code(zip_codes=['02472',
                                                                        '38120'],
                                                             dates='2021-01-01')
    assert len(watertown_new_year) == 2
    assert watertown_new_year['cases'].iloc[0] > 0
