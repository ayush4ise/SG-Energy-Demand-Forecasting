# Singapore Energy Demand Forecasting README  

This repository contains all the codes we have used to carry out our anaylsis for our paper.  

## Work done so far-  
 
### 1. Data Collection [Completed- 13/05/2023]

_Data Source_ - www.ema.gov.sg  

*Description*-   
* The data is stored in weekly files. There are 7 columns representing each day of the week and 48 rows representing each half-hourly slot of a day.    
* The data is available from the first week of 2004, starting from 5/01/2004 (Monday).  
* The data is available in pdf format only for years before 2014 and is later available in xls format too for 2014 onwards.  
* From 29/09/2014 onwards, NEM Demand Data and NEM Demand Forecast is also available for each half-hourly slot.  

*Code*-  
```data-collection.ipynb``` is a cleaner version of originally employed code to collect the data.  
It works with the current website URLs for the data from 29/09/2014 and can be used to collect all three types of data available.   
```tabula-py``` library is used to extract data from pdf files whereas ```pandas``` library is used to extract data from xls files.  

*Output*-  
* The data is collected for the years 2004 to 2022.  
* The data is stored in yearly files with columns representing days and rows representing each half-hourly slot.  
* Note that the columns not necessarily start from 1st January and end at 31st December. It starts from the first week of that year and ends at last week of that year.  
* The data is available in the folder ```data\Yearly Energy Demand Data```