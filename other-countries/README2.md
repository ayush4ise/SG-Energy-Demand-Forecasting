# README

This is a README file describing the scripts used to generate forecasts for other countries, mainly the European countries.

The GDP data for other countries is obtained from IMF's World Economic Outlook databse. The link to the database is [here](https://www.imf.org/en/Publications/WEO/weo-database/2023/October).

The energy load data for the European countries is obtained from [here](https://www.entsoe.eu/data/power-stats/).

The data is available for the years 2006 to 2024. We use the hourly data, measured in MW.

The data is stored in `other-countries/data/` directory. The data is stored in the format of a CSV file.

## The United Kingdom Case [Jan 2025]

We will make forecasts for the United Kingdom (Great Britain) for the year **2021** by using the data from the year **2011** to **2017**.

[Note: The data for the year 2018 is not available in the dataset.]

The information we will need to calculate from the data is as follows:

- Total yearly GDP in USD [`other-countries\data\GB\WEO_Data_Oct19_UK.xlsx`]
- Total yearly energy demand in MWh [*To be calculated from the data*]
- Hourly and monthly seasonality in energy demand [*To be calculated from the data*]

Steps to calculate the energy demand:

- We will aggregate the hourly data to get the total energy demand for a year.
- We will use the total GDP data and the total energy demand data till 2019 to forecast the energy demand for the year 2023.
- We will calculate the hourly and monthly seasonality in energy demand.
- We will use the seasonality to forecast the energy demand for the year 2023.
