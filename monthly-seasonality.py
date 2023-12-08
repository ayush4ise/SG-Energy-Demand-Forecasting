# This program calulates seasonality index on a monthly scale
# It uses a modified version of function sum_wdays_wends to do so
# Instead of just summing up weekday/weekend values, it also counts them and stores both values in a list

import pandas as pd
import time as tm
import datetime as dt
import numpy as np

###NOTE###
#there needs to be a small correction in one of our tables for this program to run
#In 2014.xlsx, update the column name "1506/2014..." to "15/06/2014..." 

#WE ADD ALL THE DATA FROM YEARS INTO ONE BIG DATAFRAME
#UPDATE YOUR FILE PATH ACCORDINGLY
df = pd.read_excel(r'D:\Projects\ntu-vish\Yearly Energy Demand Data\2004.xlsx')
df.set_index('Time', inplace=True) #setting time column as index
year = 2004
for i in range(1,19):
    temp_df = pd.read_excel("D:\\Projects\\ntu-vish\\Yearly Energy Demand Data\\" + str(year + i) + '.xlsx')
    temp_df.set_index('Time', inplace=True)
    df = df.merge(temp_df, left_index=True, right_index=True)

####FUNCTION TO SUM WEEKDAYS AND WEEKENDS VALUES MONTHLY
def sum_wdays_wends(row):
    sum_wdays,count_wdays = 0,0
    sum_wends,count_wends = 0,0
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
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = [sum_wdays,count_wdays]    #new column with finished month sum values
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = [sum_wends,count_wends]
                sum_wdays = row[i]      #rewriting sum_wdays for the new month
                count_wdays = 1
                sum_wends,count_wends = 0,0
            elif curr_date.tm_wday in [3,4]:
                sum_wdays += row[i]
                if curr_date.tm_wday == 3:
                    count_wdays += 2 #counting day 2 of the month Friday in previous month weekdays too
                else:
                    count_wdays += 1
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = [sum_wdays,count_wdays]
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = [sum_wends,count_wends]
                sum_wdays,count_wdays = 0,0
                sum_wends,count_wends = 0,0
            elif curr_date.tm_wday == 5:
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = [sum_wdays,count_wdays]
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = [sum_wends,count_wends]
                sum_wends = row[i]      #rewriting sum_wends for the new month
                count_wends = 1
                sum_wdays,count_wdays = 0,0
            else:
                sum_wends += row[i]
                count_wends += 1
                row[str(prev_month_year) + ' ' + prev_month + ' weekdays'] = [sum_wdays,count_wdays]
                row[str(prev_month_year) + ' ' + prev_month + ' weekends'] = [sum_wends,count_wends]
                sum_wdays,count_wdays = 0,0
                sum_wends,count_wends = 0,0
        elif curr_date.tm_mday == 2 and curr_date.tm_wday == 4: #the case where the first day is Thu and second Fri, so need to add Fri values to previous month
            row[str(prev_month_year) + ' ' + prev_month + ' weekdays'][0] += row[i]
        else:
            if curr_date.tm_wday <= 4:
                sum_wdays += row[i]
                count_wdays += 1
            else:
                sum_wends += row[i]
                count_wends += 1
    return row

df1 = df.copy() #we make a copy so that we can use the big dataframe df later
df1 = df1.apply(sum_wdays_wends, 1) #the above defined function is applied to get a dataframe with sums of weekdays and weekends on a monthly basis

#since we only need our new defined columns (month + weekdays/weekends), we separate them 
df1 = df1[df1.columns[-456:]] #(12 months * 2 categories * 19 years = 456 columns)

df3 = df1.copy() # just for the sake of conveninence while testing values

list = [] 
testdict = {}
index_list = [('Jan', 'weekdays'), ('Jan', 'weekends'), ('Feb', 'weekdays'), ('Feb', 'weekends'), ('Mar', 'weekdays'), ('Mar', 'weekends'), ('Apr', 'weekdays'), ('Apr', 'weekends'), ('May', 'weekdays'), ('May', 'weekends'),
 ('Jun', 'weekdays'), ('Jun', 'weekends'), ('Jul', 'weekdays'), ('Jul', 'weekends'), ('Aug', 'weekdays'), ('Aug', 'weekends'), ('Sep', 'weekdays'), ('Sep', 'weekends'), ('Oct', 'weekdays'),
 ('Oct', 'weekends'), ('Nov', 'weekdays'), ('Nov', 'weekends'), ('Dec', 'weekdays'), ('Dec', 'weekends')]
for i in df3.columns:
    list.append([sum([j[0] for j in df3[i]]),sum([j[1] for j in df3[i]])/len([j[1] for j in df3[i]])])
    if len(list) == 24:
        testdict[i.split()[0]] = list
        list = []
index_list = pd.MultiIndex.from_tuples(index_list)
testdf = pd.DataFrame(data = testdict, index = index_list)

#we separate weekdays and weekends dataframe for ease of calculation
wday_df = testdf.xs('weekdays',axis=0,level=1)
wend_df = testdf.xs('weekends',axis=0,level=1)

#mathematically- ( total demand for weekdays in a month / number of weekdays in month ) / ( total yearly demand for weekdays / number of weekdays in year )
for i in wday_df.columns:
    yearly_avg = sum([value_list[0] for value_list in wday_df[i]])/sum([value_list[1] for value_list in wday_df[i]])
    wday_df[i] = [value_list[0]/(value_list[1]*yearly_avg) for value_list in wday_df[i]]

for i in wend_df.columns:
    yearly_avg = sum([value_list[0] for value_list in wend_df[i]])/sum([value_list[1] for value_list in wend_df[i]])
    wend_df[i] = [value_list[0]/(value_list[1]*yearly_avg) for value_list in wend_df[i]]

# saving them in an excel file
wday_df.to_excel('S.I. Month of The Year.xlsx', sheet_name='weekdays')
with pd.ExcelWriter('S.I. Month of The Year.xlsx', mode='a', engine='openpyxl') as writer:
    wend_df.to_excel(writer, sheet_name='weekends')