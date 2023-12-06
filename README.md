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


### 2. S.I. Calculation [Completed - 10/06/2023]

**Data used**: ```data\Yearly Energy Demand Data\System Demand (Actual)\```  

**Description**:
- The yearly demand data (system actual) is utilized to calculate seasonality indices (S.I.).
- Two types of seasonality indices are computed: 
  - Half-hourly S.I. per month 
  - Hourly S.I. per month for weekdays-weekends and Mon to Fri-weekends.
- Calculation Formula:  
  - **Half-hourly SI per month (weekdays/weekends)** = 
    $\frac{\text(Average of Half-hourly demand for a month for the given time slot (weekdays/weekends))}{\text(Average of Half-hourly demand for a month across all time slots (weekdays/weekends))}$
  - Similar computation for the remaining three indices.
- Special Conditions:
  - While calculating for weekdays/weekends:
    1. If the first day of the month is Thursday or Friday, they are counted in the previous month's weekdays.
    2. If the first day of the month is Sunday, it is counted in the previous month's weekends.
- Hourly S.I. is derived by averaging S.I.s of two consecutive half-hourly time slots, treating it as an hourly slot. _(This is mathematically equivalent to the SI obtained using the formula.)_

**Code**:
The ```seasonality-calculation.py``` file executes these calculations. Users can employ this file by updating the file paths accordingly within the code.

**Output**:
- Four Excel files are generated, each containing yearly sheets.
- Rows depict time slots, while columns represent weekdays/weekends for each month.
- The data is located in the folder named ```data\Seasonality Index Data\```.