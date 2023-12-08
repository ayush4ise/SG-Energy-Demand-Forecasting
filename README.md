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
    $\frac{\text{Average of Half-hourly demand for a month for the given time slot (weekdays/weekends)}}{\text{Average of Half-hourly demand for a month across all time slots (weekdays/weekends)}}$
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


### 3. ANOVA tests [Completed - 24/06/2023]

**Data used**: ```data\Yearly Energy Demand Data\System Demand (Actual)\```

**Description**:
- One-way ANOVA tests were conducted to assess the consistency of seasonality indices over consecutive 3-year periods.
- Results were gathered in blocks of 3 years (e.g., 2005-2007, 2008-2010, etc.).
- Testing Details:
  - Null Hypothesis ($H_0$): S.I. values for a given time slot remain constant over 3 years.
  - Alternate Hypothesis ($H_1$): S.I. values show significant variation.
- Tests were performed separately for one, two, three, and four-hour groups, considering weekdays and weekends independently.

**Code**:  
The ```anova-tests.py``` file facilitates these computations and stores the results. Users can utilize the code by adjusting the file paths within the script and specifying the hour group of interest.

**Output**:
- Four Excel files are generated for each hour group.
- Each Excel file contains sheets representing the 3-year blocks.
- The data is located in the folder named ```data\3 Year ANOVA\```.


### 4. T-tests

#### [Completed - 01/07/2023]

**Data used**: ```Hourly SI per Month(Weekdays,Weekends).xlsx```

**Description**: 
- Conducted one sample two-tailed t-tests to compare the absolute difference between a given hour's S.I. across two consecutive years against a specified value (population mean).
- Results calculated separately for weekdays and weekends.
- Testing Details:
  - Null Hypothesis ($H_0$): Absolute difference between S.I. values for a given time slot = 0.005.
  - Alternate Hypothesis ($H_1$): Difference is not equal to 0.005.

**Code**: 
The ```ttest_1samp2tail.py``` file performs these computations and stores the results. To use, update the file paths in the script and specify the day type (weekdays/weekends).

**Output**: 
Two Excel files are generated for each day type:
- ```Consolidated t-test results [weekdays].xlsx```
- ```Consolidated t-test results [weekends].xlsx```
Located in the folder named ```data\3 Year ANOVA\t-testing```.

---

#### [Completed - 06/07/2023]

**Data used**: ```data\Seasonality Index Data\```

**Description**: 
- Executed two sample one-tailed t-tests to determine the population mean value (difference in S.I.s) for which the null hypothesis ($H_0$) is rejected across consecutive yearly pairs.
- Details of the t-test are available in the file ```ttesting-sample.ipynb```.
- Population mean values were determined through trial and error.

**Code**: 
The `ttest_2samp1tail.py` file contains version 1.0, which is commented out in the code. This version is used for executing the computations by adjusting the file paths as indicated, while the subsequent code is commented out.

**Output**:
The tests were performed for all consecutive yearly pairs, determining population mean values for each case. Results are as follows:

  **Hourly Weekdays**: 0.0184, **Weekends**: 0.0185
  **Mon**: 0.0215, **Tue**: 0.0229, **Wed**: 0.0229, **Thu**: 0.0202, **Fri**: 0.0271
  **Half-Hourly Weekdays**: 0.0209, **Weekends**: 0.0186
  **Mon**: 0.0228, **Tue**: 0.0231, **Wed**: 0.0236, **Thu**: 0.0209, **Fri**: 0.0283

11/07/2023:
Data used: Hourly SI (Weekdays,Weekends)
Description: finding popmean for which H0 gets rejected for all yearly pairs for each hour
Code: ttesting.py [v2.0] [take updated one from github]
Output: t-test results (all possible pairs)

14/07/2023:
Data used: Yearly Energy Demand Data
Description: finding monthly seasonality
Formula- avg daily demand in a month (weekdays)/avg daily demand in an year (weekdays) [similarly for weekends]
also, follows the special condition mentioned in seasonality
Code: monthly-seasonality.py [based off seasonality-calculation.py]
Output: S.I. Month of the Year ([Corrected] in Drive)

Also, 
perform t-tests [finding popmean for which H0 gets rejected for all yearly pairs]
Code: ttesting.py [v2.1] [get from github]
Output: Monthly SI t-test results

02/08/2023:
Data Used: Yearly Energy Demand Data
Description: scaling the SIs (new formulas)
Formulas- [check once again with Juan ppt]
SI for Month of the Year = avg daily demand for month/avg daily demand for year for a particular time slot
SI for Day of the Week = avg daily demand for Mondays for a month/avg daily demand for the month * monthlySI 
SI for Hour of the Day = avg hourly demand for a given hour of Mondays for a month/avg hourly demand of Mondays for a momth * monthlySI * weekly SI
Code: seasonality[01.08].ipynb 
Output:
[under New SI data in Drive]
SI for Month of the Year
SI for Day of the Week
SI for Hour of the Day

17/08/2023:
Description:
basic definition of the proposed ES model
Code: model_definition.ipynb [update it to remove doubts and issues]
models.py

06/09/2023:
Description: hourlySI scaled with just monthlySI, t-tests for the same
Code: employed some old code with some necessary changes

24/09/2023:
Description: alpha,beta = 0.2,0.8 (found), tested es model for the first time
Code: mehhhh, let's see

26/09/2023:
Description: linreg models output
Code: gdp_popgrowth something something on Drive
Output: forecast 2018 [Drive]

--decision to use unscaled SIs only--
[add this detail into "data used"]

--NEM data collection, but not that big of a work--

10/2023:
Description: multiple models and results collection
Code: pipelines, utils_ts, .ipynbs 

11/2023:
Description: experiment with 5Y inputs
Code: updated pipelines in .ipynb,5y-input, es-issues and sarimax-trouble for code on Github [although same code, just tweaked input]

MAPE VALUE TABLE