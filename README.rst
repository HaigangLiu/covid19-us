======================
covid19-us
======================

.. image:: https://img.shields.io/pypi/v/covid19_us.svg
        :target: https://pypi.python.org/pypi/covid19-us

.. image:: https://img.shields.io/travis/HaigangLiu/covid19-us.svg
        :target: https://travis-ci.com/HaigangLiu/covid19-us



* This package aims to provide a streamlined way to download covid data. We support the historical data sliced by state and county. We also support zip code as valid input type, but the covid counts is from the county where the zip code area is in.

* Free software: MIT license

Features
--------

1. Download data by state in the United States

    :code:`get_daily_data()` is a function to download daily data from a given state. An example is illustrated as follows. Note that the following functions typically can accept both list type or string type. In other words, ['SC'] and 'SC' can be both understood as South Carolina correctly.

.. code-block:: python3

       from covid19_us.download import get_daily_data
       sc_xmas = get_daily_data('SC', dates=['2020-12-31', '2021-01-01'])

2. Download data by county in the United States

    :code:`get_daily_data_by_county()` is a function to download daily data from a given county or counties. An example is illustrated as follows. We support both county name and county FIPS, a unique identifier.

.. code-block:: python3

       from covid19_us.download import get_daily_data_by_county
       sc_new_year = get_daily_data_by_county('SC', counties='Richland', dates=['2020-12-31']))

3. Download data by zip code in the United States

    :code:`get_daily_data_by_zipcode()` is function to download daily data from a given zip code. Again, this is not exactly count by zip code, but the county total where the zip code resides in.

.. code-block:: python3

       from covid19_us.download import get_daily_data_by_zip_code
       tn_new_year = get_daily_data_by_zip_code('TN', zip_codes=['38120'] dates=['2021-01-01'])



