# Singapore Energy Demand Forecasting README  

This repository contains all the codes used for our analysis in the paper.  

## Work Completed So Far  
 
### 1. Data Collection [Completed - 13/05/2023]

**Data Source**: [www.ema.gov.sg](www.ema.gov.sg)  

**Description**:  
- The data is structured in weekly files, with 7 columns representing each day of the week and 48 rows representing half-hourly slots in a day.    
- Availability starts from the first week of 2004, beginning on 5/01/2004 (Monday).  
- Data was initially available only in PDF format for years before 2014; later, from 2014 onwards, it became available in XLS format as well.  
- Starting from 29/09/2014, NEM Demand Data and NEM Demand Forecast are included for each half-hourly slot.  

**Code**:  
The ```data-collection.ipynb``` file is an improved version of the original code used for data collection. It is compatible with the current website URLs for data retrieval from 29/09/2014 onwards and can collect all three types of available data. It utilizes the ```tabula-py``` library to extract data from PDF files and the ```pandas``` library to extract data from XLS files.

**Output**:  
- Collected data spans from the years 2004 to 2022.  
- Yearly data is stored in files with columns representing days and rows representing half-hourly slots.  
- Note that columns may not necessarily span from 1st January to 31st December; they start from the first week and end at the last week of each year.  
- The data is located in the folder named ```data\Yearly Energy Demand Data```.
