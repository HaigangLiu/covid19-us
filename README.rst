======================
covid19-us
======================

.. image:: https://img.shields.io/pypi/v/covid19_us.svg
        :target: https://pypi.python.org/pypi/covid19-us

.. image:: https://img.shields.io/travis/HaigangLiu/covid19-us.svg
        :target: https://travis-ci.com/HaigangLiu/covid19-us

Overview
--------

This package aims to provide a streamlined way to download historical covid data from the United States. We support the historical data sliced by state, county and zip code through three easy-to-use APIs: `download_by_state`, `download_by_county` and `download_by_zip_code`.

Note that for most input variables, we support either a string or a list. For example, 'zip_code_list' can be either `38120` or `['38120', '02472']`. If it's the latter case, two result sets will be concatenated and returned as a pandas dataframe.

Free software: MIT license

Features
--------

1. Download data by state in the United States

    :code:`download_by_state()` is a function to download daily data from a given state. An example is illustrated as follows. Note that the following functions typically can accept both list type or string type. In other words, `['SC']` and `SC` can be both understood as South Carolina correctly.

.. code-block:: python3

       from covid19_us import download_by_state
       sc_three_days = download_by_state(state='SC', dates=['2020-12-31', '2021-01-01', '2021-01-02'])
       sc_three_days[['state', 'date', 'cases', 'deaths']]


+---+-------+---------------------+-------+--------+
|   | state | date                | cases | deaths |
+---+-------+---------------------+-------+--------+
| 0 | SC    | 2021-01-02 00:00:00 | 5211  | 89     |
+---+-------+---------------------+-------+--------+
| 1 | SC    | 2021-01-01 00:00:00 | 0     | 0      |
+---+-------+---------------------+-------+--------+
| 2 | SC    | 2020-12-31 00:00:00 | 4032  | 47     |
+---+-------+---------------------+-------+--------+


2. Download data by county in the United States

    :code:`download_by_county()` is a function to download daily data from a given county or counties. An example is illustrated as follows. We support both county name and county FIPS, a unique identifier.

.. code-block:: python3

       from covid19_us import download_by_county
       from pandas import date_range
       richland_2020 = download_by_county(states='SC', counties='Richland', dates=date_range('2021-02-10', '2021-02-15'))

+--------+----------+---------------------+--------+-------+-------------------+------------------+
|        | county   | date                | deaths | cases | deaths_cumulative | cases_cumulative |
+--------+----------+---------------------+--------+-------+-------------------+------------------+
| 888738 | Richland | 2021-02-10 00:00:00 | 5      | 173   | 457               | 37804            |
+--------+----------+---------------------+--------+-------+-------------------+------------------+
| 888739 | Richland | 2021-02-11 00:00:00 | 3      | 208   | 460               | 38012            |
+--------+----------+---------------------+--------+-------+-------------------+------------------+
| 888740 | Richland | 2021-02-12 00:00:00 | 1      | 239   | 461               | 38251            |
+--------+----------+---------------------+--------+-------+-------------------+------------------+
| 888741 | Richland | 2021-02-13 00:00:00 | 2      | 239   | 463               | 38490            |
+--------+----------+---------------------+--------+-------+-------------------+------------------+
| 888742 | Richland | 2021-02-14 00:00:00 | 3      | 312   | 466               | 38802            |
+--------+----------+---------------------+--------+-------+-------------------+------------------+
| 888743 | Richland | 2021-02-15 00:00:00 | 6      | 164   | 472               | 38966            |
+--------+----------+---------------------+--------+-------+-------------------+------------------+

3. download data by zip code in the united states

    :code:`download_by_zip_code()` is function to download daily data from a given zip code. Again, this is not exactly count by zip code, but the county total where the zip code resides in.


.. code-block:: python3

       from covid19_us import download_by_zip_code
       tn_new_year = download_by_zip_code(zip_code_list=['38120'], dates=['2021-01-01', '2021-01-02', '2021-01-03'])

+--------+--------+-------+-------+---------------------+-------------------+------------------+--------+-------+
|        | county | state | fips  | date                | deaths_cumulative | cases_cumulative | deaths | cases |
+--------+--------+-------+-------+---------------------+-------------------+------------------+--------+-------+
| 953003 | Shelby | TN    | 47157 | 2021-01-01 00:00:00 | 903               | 67800            | 0      | 602   |
+--------+--------+-------+-------+---------------------+-------------------+------------------+--------+-------+
| 953004 | Shelby | TN    | 47157 | 2021-01-02 00:00:00 | 914               | 69798            | 11     | 1998  |
+--------+--------+-------+-------+---------------------+-------------------+------------------+--------+-------+
| 953005 | Shelby | TN    | 47157 | 2021-01-03 00:00:00 | 925               | 70142            | 11     | 344   |
+--------+--------+-------+-------+---------------------+-------------------+------------------+--------+-------+

Credits
-------
- The data source is from `the New York Times <https://www.nytimes.com/interactive/2021/us/tennessee-covid-cases.html>`_. The author would also like to express his gratitude for the agency's effort to achieve outstanding journalism.

