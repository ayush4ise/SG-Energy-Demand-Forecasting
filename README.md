# Singapore Energy Demand Forecasting README  

This repository contains all the codes used for our analysis in the paper.  

## Work Completed So Far  
 
### 1. Data Collection [Completed - 13/05/2023]

**Data Source**: www.ema.gov.sg

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
    $\frac{\text{Average of half-hourly demand for a month for the given time slot (weekdays/weekends)}}{\text{Average of half-hourly demand for a month across all time slots (weekdays/weekends)}}$
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

**Data used**: ```data\Seasonality Index Data\Hourly SI per Month(Weekdays,Weekends).xlsx```

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
The tests were performed for all consecutive yearly pairs, determining population mean values (upto 3 decimal places) for each case. Results are as follows:

  **Hourly Weekdays**: 0.0184, **Weekends**: 0.0185  
  **Mon**: 0.0215, **Tue**: 0.0229, **Wed**: 0.0229, **Thu**: 0.0202, **Fri**: 0.0271  
  **Half-Hourly Weekdays**: 0.0209, **Weekends**: 0.0186  
  **Mon**: 0.0228, **Tue**: 0.0231, **Wed**: 0.0236, **Thu**: 0.0209, **Fri**: 0.0283  

---

#### [Completed - 11/07/2023]

**Data used**: ```data\Seasonality Index Data\Hourly SI per Month(Weekdays,Weekends).xlsx```

**Description**:
- Conducted t-tests following the methodology from previous work [06/07/2023].
- Tests performed for all possible yearly pairs.

**Code**:  
The `ttest_2samp1tail.py` file contains version 2.0, which is commented out in the code. This version is used for executing the computations by adjusting the file paths as indicated, while the subsequent code is commented out.

**Output**: 
- Performed tests for all possible yearly pairs, determining population mean values (up to 3 decimal places) for each case.
- Results stored in ```data\t-testing\Hourly S.I. t-test results (all possible pairs).xlsx```.


### 5. New S.I. Calculation 

#### [Completed - 14/07/2023]

**Data used**: ```data\Yearly Energy Demand Data\System Demand (Actual)\```

**Description**: 
- Computed monthly seasonality indices using the formula:
  - Monthly S.I. = $\frac{\text{Average daily demand in a month (weekdays/weekends)}}{\text{Average daily demand in a year (weekdays/weekends)}}$
- Followed special conditions mentioned in "2. S.I. Calculation".
- Conducted t-tests using the methodology from previous work [06/07/2023] for all possible yearly pairs.

**Code**: 
- The file ```monthly-seasonality.py``` executes the computations and saves the results by adjusting the input file paths accordingly. It is based on ```seasonality-calculation.py```.
- Version 2.1 in `ttest_2samp1tail.py` is used for executing t-tests by adjusting the file paths, performing the computations, and saving the results.

**Output**: 
- Monthly seasonalities stored in ```data\New SI Data\S.I. Month of the Year.xlsx```
- t-test results stored in ```data\t-testing\Monthly S.I. t-test results.xlsx```

---

#### [Completed - 02/08/2023]

**Data Used**: ```data\Yearly Energy Demand Data\System Demand (Actual)\```

**Description**: 
- The seasonality indices are scaled by the higher seasonality indices. 
- Formulas
  - SI for the Month = $\frac{\text{Average daily demand for month}}{\text{Average daily demand for year}}$
  - Overall SI for the Month = $\frac{\sum_{i=2004}^{2022} \text{SI for the Month}}{2022-2004+1}$

  - SI for Day of the Week = $\frac{\text{Average daily demand for Mondays of a month}}{\text{Average daily demand for the month} * \text{Overall Monthly SI}}$
  - Overall SI for Day of the Week = $\frac{\sum_{i=2004}^{2022} \sum_{j=Jan}^{Dec} \text{SI for Day of the Week}}{Number of Month and Year combinations}$

  - SI for Hour of the Day = $\frac{\text{Average hourly demand for a given hour for Mondays of a month}}{\text{Average hourly demand for Mondays of the month} * \text{Overall Monthly SI} * \text{Overall Weekly SI}}$
  - Overall SI for Hour of the Day = $\frac{\sum_{i=2004}^{2022} \sum_{j=Jan}^{Dec} \sum_{k=Mon}^{Sun} \text{SI for Hour of the Day}}{Number of Month,Year,Day combinations}$

**Code**:  
The file ```scaled-seasonality.ipynb``` performs computations and saves the results after changing the input file paths accordingly.

**Output**:  
The following Excel files are generated:
- ```S.I. for the Month.xlsx```
- ```S.I. Day of the Week.xlsx```
- ```S.I. Hour of the Day.xlsx```  
Located in the folder named ```data\New SI Data\```


### 6. Model Definition 

#### [Completed - 17/08/2023]

**Description**:
- The proposed ES model is defined. 
- Details of the model are available in the file ```model-definition.ipynb```.
- Initial parameters are yet to be found.

**Code**: 
- The file ```model_definition.ipynb``` stores the basic definition of the proposed ES model.  

---

#### [Completed - 06/09/2023]

**Description**: 
- Decision made to omit the day of the week seasonality from the model.
- S.I. for Hour of the Day recalculated by scaling with just S.I. for the Month.
- Conducted t-tests using the methodology from previous work [06/07/2023] for all possible yearly pairs.

**Code**:  
- Utilized ```scaled-seasonality.ipynb``` and ```ttest_2samp1tail.py``` with necessary changes as required for the updated calculations.

**Output**:
- ```Hourly SI [excluding Daily SI].xlsx``` stored in folder ```data\New SI Data\```
- ```t-test results [scaled SIs].xlsx``` stored in folder ```data\t-testing\```

---

#### [Completed - 24/09/2023]

**Data**: 
- ```data\Model Inputs\i_sh[scaled].txt```,```data\Model Inputs\i_sm.txt```
- ```data\Yearly Energy Demand Data\System Demand (Actual)\```

**Description**:
- First-time testing of the ES model to forecast 2018 demand.
- Seasonalities are assumed to be constant and are not updated in the model.
- Data for the forecasted year is assumed to be unknown.
- Initial seasonalities taken as the average of seasonality data from 2011 to 2017.
- Input timeseries data is considered for the years 2011 to 2017.
- Utilized a 100*100 search grid to find alpha and beta parameter values for the least Mean Absolute Percentage Error (MAPE):  
  $\alpha$ = 0.19, $\beta$ = 0.88

**Code**: 
- Use the `constant_seasonality_model` function from the file ```models.py``` for the model.
- File ```utils_ts.py``` is available to convert energy demand data into usable timeseries data for the input and test series.

---

#### [Completed - 26/09/2023]

**Data**: 
- ```data\Model Inputs\i_sh[scaled].txt```, ```data\Model Inputs\i_sm.txt```
- ```data\Model Inputs\Population Growth.xlsx``` [Source - www.singstat.gov.sg ]
- ```data\Model Inputs\Total Yearly Demand.xlsx``` [Source - www.singstat.gov.sg ]

**Description**: 
- Defined three linear regression models for comparison with the ES model.
- Models are used to forecast total yearly demand, then further employed to make hourly demand forecasts.
- Formula Used:  
  Hourly Demand = $\frac{\text{Total Yearly Demand}}{365*24} * \text{Monthly SI} * \text{Daily SI}$
- Models:
  - First model uses the relationship between GDP vs Total Yearly Demand.
  - Second model uses the relationship between Population Growth vs Total Yearly Demand.
  - Third model uses the relationship between both GDP and Population Growth vs Total Yearly Demand.

**Code**:
- Utilize ```gdp-model.py``` and ```population-model.py``` to forecast and save 2018 hourly demand data, adjusting the file paths accordingly.

---

It was decided to utilize only unscaled Seasonal Indices (SIs) for the ongoing analyses and forecasting models.

---

NEM (Net Energy Metering) data was collected to facilitate a comparative analysis.

---


### 7. Model Comparison [Completed - 10/2023]

**Description**: 
- Multiple models were utilized for comparison, including FBProphet, SARIMAX, MSTL+ARIMA, and Dynamic Harmonic Regression.
- NEM Forecasts were considered for the NEM demand data alongside the ES model, assuming knowledge of the forecast year's demand.
- Forecasts were generated, and Mean Absolute Percentage Error (MAPE) values were recorded for the years 2018 to 2022.

**Code**: 
- ```utils_ts.py``` handles input and test series.
- ```models.py``` contains ES models.
- ```pipelines.py``` stores pipelines for all models to calculate forecasts and record results.
- ```yearly-forecasts-for-table.ipynb``` shows how the values for the MAPE table are calculated.

### 8. 5Y Input Experiment [Completed - 11/2023]

**Description**: 
- Previously, models were trained with data from 2011 to (forecast year - 1), causing overfitting in some models like SARIMAX, resulting in suboptimal performance.
- An experiment was conducted using only the previous 5 years' data as input for forecasting. For instance, for predicting 2018 data, input consisted of data from 2013 to 2017; for 2019, data from 2014 to 2018, and so forth.
- This experiment excluded linear regression models, as these models generally benefit from more data.

**Code**:  
The same codes used in the previous section [7. Model Comparison] were employed with adjustments to limit the input data to the last 5 years.