import pandas as pd
import time as tm
import datetime as dt
import numpy as np

###NOTE###
#there needs to be a small correction in one of our tables for this program to run
#In 2014.xlsx, update the column name "1506/2014..." to "15/06/2014..." 

#WE ADD ALL THE DATA FROM YEARS INTO ONE BIG DATAFRAME
#UPDATE YOUR FILE PATH ACCORDINGLY
df = pd.read_excel('./Yearly Energy Demand Data/2004.xlsx')
df.set_index('Time', inplace=True) #setting time column as index
year = 2004
for i in range(1,19):
    temp_df = pd.read_excel('./Yearly Energy Demand Data/' + str(year + i) + '.xlsx')
    temp_df.set_index('Time', inplace=True)
    df = df.merge(temp_df, left_index=True, right_index=True)

####FUNCTION TO SUM WEEKDAYS AND WEEKENDS VALUES MONTHLY
def sum_wdays_wends(row):
    sum_wdays = 0
    sum_wends = 0
    for i in df.columns:
        curr_date = tm.strptime(i,"%d/%m/%Y\n%a")
        if curr_date.tm_mon == 1: #a measure for 1st of January values that should be added to December
            prev_month = 'Dec'
            prev_month_year = curr_date.tm_year-1
        else:
            prev_month = tm.strftime("%b",tm.strptime(str(curr_date.tm_mon-1), "%m"))
            prev_month_year = curr_date.tm_year
        if curr_date.tm_mday == 1:      #first of the month
            if curr_date.tm_wday in [0,1,2]:        #month starts from mon, tue, wed
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = sum_wdays    #new column with finished month sum values
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_wdays = row[i]      #rewriting sum_wdays for the new month
                sum_wends = 0
            elif curr_date.tm_wday in [3,4]:
                sum_wdays += row[i]
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = sum_wdays
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_wdays = 0
                sum_wends = 0
            elif curr_date.tm_wday == 5:
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = sum_wdays
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_wends = row[i]      #rewriting sum_wends for the new month
                sum_wdays = 0
            else:
                sum_wends += row[i]
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = sum_wdays
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_wdays = 0
                sum_wends = 0
        elif curr_date.tm_mday == 2 and curr_date.tm_wday == 4: #the case where the first day is Thu and second Fri, so need to add Fri values to previous month
            row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] += row[i]
        else:
            if curr_date.tm_wday <= 4:
                sum_wdays += row[i]
            else:
                sum_wends += row[i]
    return row

####FUNCTION TO SUM WEEKDAYS (Mon-Fri separately) AND WEEKEND VALUES MONTHLY
def sum_mon_fri_wends(row):
    sum_mon = 0
    sum_tue = 0
    sum_wed = 0
    sum_thu = 0
    sum_fri = 0
    sum_wends = 0
    for i in df.columns:
        curr_date = tm.strptime(i,"%d/%m/%Y\n%a")
        if curr_date.tm_mon == 1: #a measure for 1st of January values that should be added to December
            prev_month = 'Dec'
            prev_month_year = curr_date.tm_year-1
        else:
            prev_month = tm.strftime("%b",tm.strptime(str(curr_date.tm_mon-1), "%m"))
            prev_month_year = curr_date.tm_year
        if curr_date.tm_mday == 1:      #first of the month
            if curr_date.tm_wday in [0,1,2]:        #month starts from mon, tue, wed
                row[str(prev_month_year) + ' ' + prev_month + ' Mon'] = sum_mon    #new column with finished month sum values
                row[str(prev_month_year) + ' ' + prev_month + ' Tue'] = sum_tue
                row[str(prev_month_year) + ' ' + prev_month + ' Wed'] = sum_wed
                row[str(prev_month_year) + ' ' + prev_month + ' Thu'] = sum_thu
                row[str(prev_month_year) + ' ' + prev_month + ' Fri'] = sum_fri
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                if curr_date.tm_wday == 0:
                    sum_mon,sum_tue,sum_wed,sum_thu,sum_fri = row[i],0,0,0,0
                elif curr_date.tm_wday == 1:
                    sum_mon,sum_tue,sum_wed,sum_thu,sum_fri = 0,row[i],0,0,0
                else:
                    sum_mon,sum_tue,sum_wed,sum_thu,sum_fri = 0,0,row[i],0,0
                sum_wends = 0
            elif curr_date.tm_wday in [3,4]:
                if curr_date.tm_wday == 3:
                    sum_thu += row[i]
                else:
                    sum_fri += row[i]
                row[str(prev_month_year) + ' ' + prev_month + ' Mon'] = sum_mon   
                row[str(prev_month_year) + ' ' + prev_month + ' Tue'] = sum_tue
                row[str(prev_month_year) + ' ' + prev_month + ' Wed'] = sum_wed
                row[str(prev_month_year) + ' ' + prev_month + ' Thu'] = sum_thu
                row[str(prev_month_year) + ' ' + prev_month + ' Fri'] = sum_fri
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_mon,sum_tue,sum_wed,sum_thu,sum_fri = 0,0,0,0,0
                sum_wends = 0
            elif curr_date.tm_wday == 5:
                row[str(prev_month_year) + ' ' + prev_month + ' Mon'] = sum_mon   
                row[str(prev_month_year) + ' ' + prev_month + ' Tue'] = sum_tue
                row[str(prev_month_year) + ' ' + prev_month + ' Wed'] = sum_wed
                row[str(prev_month_year) + ' ' + prev_month + ' Thu'] = sum_thu
                row[str(prev_month_year) + ' ' + prev_month + ' Fri'] = sum_fri
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_wends = row[i]      #rewriting sum_wends for the new month
                sum_mon,sum_tue,sum_wed,sum_thu,sum_fri = 0,0,0,0,0
            else:
                sum_wends += row[i]
                row[str(prev_month_year) + ' ' + prev_month + ' Mon'] = sum_mon   
                row[str(prev_month_year) + ' ' + prev_month + ' Tue'] = sum_tue
                row[str(prev_month_year) + ' ' + prev_month + ' Wed'] = sum_wed
                row[str(prev_month_year) + ' ' + prev_month + ' Thu'] = sum_thu
                row[str(prev_month_year) + ' ' + prev_month + ' Fri'] = sum_fri
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = sum_wends
                sum_mon,sum_tue,sum_wed,sum_thu,sum_fri = 0,0,0,0,0
                sum_wends = 0
        elif curr_date.tm_mday == 2 and curr_date.tm_wday == 4: #the case where the first day is Thu and second Fri, so need to add Fri values to previous month
            row[str(prev_month_year) + ' ' + prev_month + ' Fri'] += row[i]
        else:
            if curr_date.tm_wday == 0:
                sum_mon += row[i]
            elif curr_date.tm_wday == 1:
                sum_tue += row[i]
            elif curr_date.tm_wday == 2:
                sum_wed += row[i]
            elif curr_date.tm_wday == 3:
                sum_thu += row[i]
            elif curr_date.tm_wday == 4:
                sum_fri += row[i]
            else:
                sum_wends += row[i]
    return row

df1 = df.copy() #we make a copy so that we can use the big dataframe df later
df2 = df.copy() #df2 for (mon-fri, weekdays) table
df1 = df1.apply(sum_wdays_wends, 1) #the above defined function is applied to get a dataframe with sums of weekdays and weekends on a monthly basis
df2 = df2.apply(sum_mon_fri_wends,1)

#since we only need our new defined columns (month + weekdays/weekends), we separate them 
df1 = df1[df1.columns[-456:]] #(12 months * 2 categories * 19 years = 456 columns)
df2 = df2[df2.columns[-1368:]] #(12 months * 6 categories * 19 years = 1368 columns)

df3 = df1.copy() #we need this df1 here to work on for our month of the year table, so we create a copy

#seasonality indexes calculated from averages
# sum(time slot)/(no. of days) / sum(total)/(no.of days * 48 timeslots) == sum(time slot) * 48 / sum(total)
for i in df1.columns:
    df1[i] = df1[i]*48/sum(df1[i])
for j in df2.columns:
    df2[j] = df2[j]*48/sum(df2[j])

#multi-index columns created for easier tables
columns = []
for i in df1.columns:
    columns.append(tuple(i.split()))
columns = pd.MultiIndex.from_tuples(columns)
df1.columns = columns
columns2 = []
for i in df2.columns:
    columns2.append(tuple(i.split()))
columns2 = pd.MultiIndex.from_tuples(columns2)
df2.columns = columns2

#saving them into an excel file with year-wise sheets
temp_df = df1.xs(str(year), axis=1, level=0) #year = 2004, already defined on line 10
temp_df2 = df2.xs(str(year), axis=1, level=0)
temp_df.to_excel('Half-Hourly S.I. per Month(Weekdays,Weekends).xlsx', sheet_name=str(year))
temp_df2.to_excel('Half-Hourly S.I. per Month(Mon-Fri,Weekends).xlsx', sheet_name=str(year))
for i in range(1, 19):
    temp_df = df1.xs(str(year + i), axis=1, level=0)
    temp_df2 = df2.xs(str(year + i), axis=1, level=0)
    sheet_name = str(year + i)
    with pd.ExcelWriter('Half-Hourly S.I. per Month(Weekdays,Weekends).xlsx', mode='a', engine='openpyxl') as writer:
        temp_df.to_excel(writer, sheet_name=sheet_name)
    with pd.ExcelWriter('Half-Hourly S.I. per Month(Mon-Fri,Weekends).xlsx', mode='a', engine='openpyxl') as writer:
        temp_df2.to_excel(writer, sheet_name=sheet_name)    

####TO GET HOURLY TABLES, WE CAN USE THE HALF-HOURLY CALCULATED SEASONALITY INDEXES
#mathematically, hourly indexes were the average of two consecutive half-hourly indexes
tempdf = pd.read_excel("Half-Hourly S.I. per Month(Weekdays,Weekends).xlsx",sheet_name='2004',header=[0,1], index_col=0)
tempdf2 = pd.read_excel("Half-Hourly S.I. per Month(Weekdays,Weekends).xlsx",sheet_name='2004',header=[0,1], index_col=0)
drop_list = []
for i in range(48):
    if i%2 == 1:
        tempdf.iloc[i] = (tempdf.iloc[i] + tempdf.iloc[i-1])/2
        tempdf2.iloc[i] = (tempdf2.iloc[i] + tempdf2.iloc[i-1])/2
    else:
        drop_list.append(tempdf.index[i])
tempdf.drop(drop_list,inplace=True)
tempdf.to_excel('Hourly S.I. per Month(Weekdays,Weekends).xlsx', sheet_name=str(year))
tempdf2.drop(drop_list,inplace=True)
tempdf2.to_excel('Hourly S.I. per Month(Mon-Fri,Weekends).xlsx', sheet_name=str(year))

#saving them into an excel file with year-wise sheets
for i in range(1,19):
    tempdf = pd.read_excel("Half-Hourly S.I. per Month(Weekdays,Weekends).xlsx",sheet_name=str(year+i),header=[0,1], index_col=0)
    tempdf2 = pd.read_excel("Half-Hourly S.I. per Month(Mon-Fri,Weekends).xlsx",sheet_name=str(year+i),header=[0,1], index_col=0)
    for j in range(48):
        if j%2 == 1:
            tempdf.iloc[j] = (tempdf.iloc[j] + tempdf.iloc[j-1])/2
            tempdf2.iloc[j] = (tempdf2.iloc[j] + tempdf2.iloc[j-1])/2
    tempdf.drop(drop_list,inplace=True)
    tempdf2.drop(drop_list,inplace=True)
    sheet_name = str(year + i)
    with pd.ExcelWriter('Hourly S.I. per Month(Weekdays,Weekends).xlsx', mode='a', engine='openpyxl') as writer:
        tempdf.to_excel(writer, sheet_name=sheet_name)
    with pd.ExcelWriter('Hourly S.I. per Month(Mon-Fri,Weekends).xlsx', mode='a', engine='openpyxl') as writer:
        tempdf2.to_excel(writer, sheet_name=sheet_name)