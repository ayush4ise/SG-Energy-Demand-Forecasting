def filepath(year:int,demandtype:str):
    """
    Works for the following file structure-

    ├── yourfile
    ├── Yearly Energy Demand Data/
    │ ├── System Demand (Actual)
    │ └── NEM Demand (Actual)
    | └── NEM Demand (Forecast)

    demandtype = ['system','nem_actual','nem_forecast']
    """
    typelist = ['system','nem_actual','nem_forecast']
    if demandtype == typelist[0]:
        return "Yearly Energy Demand Data/System Demand (Actual)/" + f"{year}.xlsx"
    elif demandtype == typelist[1]:
        return "Yearly Energy Demand Data/NEM Demand (Actual)/" + f"{year}[nem_actual].xlsx"
    elif demandtype == typelist[2]:
        return "Yearly Energy Demand Data/NEM Demand (Forecast)/" + f"{year}[nem_forecast].xlsx"
    else:
        pass

def timeseries(startyear:int, endyear:int, demandtype:str):
    """
    works when filepath function is supported for the file

    typelist = ['system','nem_actual','nem_forecast']
    """
    import warnings
    warnings.filterwarnings("ignore")

    import numpy as np
    import pandas as pd
    import datetime as dt
    # collect all years of data in one dataframe
    bigdf = pd.read_excel(filepath(startyear-1,demandtype), index_col=0)
    for year in range(startyear,endyear+1):
        temp_df = pd.read_excel(filepath(year,demandtype), index_col=0)
        bigdf = bigdf.merge(temp_df, left_index=True, right_index=True)

    # turn it into a timeseries data with proper date and time index
    datelist = []
    delta = dt.timedelta(minutes=30) # to fix half-hourly slots, to make them start at 00:00 and end at 23:30 
    for i in bigdf.columns:
        for j in bigdf.index:
            j_mod = dt.datetime.strptime(j,"%H:%M") - delta
            j_mod = dt.datetime.strftime(j_mod," %H:%M")
            datelist.append(i[:11]+j_mod)

    bigdf = bigdf.melt()
    bigdf['variable'] = pd.to_datetime(datelist, dayfirst=True)
    bigdf.set_index('variable', inplace=True)
    bigdf = bigdf[bigdf.index.year >= startyear]
    bigdf = bigdf[bigdf.index.year <= endyear]

    # turning it into hourly data
    tempdf = bigdf.copy()
    drop_list = []
    for i in range(len(tempdf)):
        if i%2 == 0:
            tempdf.iloc[i] = (tempdf.iloc[i] + tempdf.iloc[i+1])
        else:
            drop_list.append(tempdf.index[i])
    tempdf.drop(drop_list,inplace=True)

    return tempdf