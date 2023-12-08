import pandas as pd
from scipy import stats
import math

# function that takes two arrays as inputs and performs both the t-tests and announces the result
# put the function in use in a loop for all year pairs and hours

def ttest(sample1,sample2,popmean):
    # mean of samples
    x1 = sample1.mean()
    x2 = sample2.mean()
    # number of observations
    n1 = sample1.size
    n2 = sample2.size
    # standard deviation
    s1 = sample1.std()
    s2 = sample2.std()
    # pooled standard deviation
    sp = math.sqrt(((n1-1)*(s1**2) + (n2-1)*(s2**2))/(n1+n2-2))
    # calculated for the alpha value of 0.05 and degrees of freedom (n1+n2-2)
    crit_value = stats.t.ppf(1-0.05,n1+n2-2)
    # left tailed t-test
    # popmean > 0 
    t_left = ((x1-x2)-popmean)/(sp*math.sqrt((1/n1)+(1/n2)))
    # right tailed t-test
    # popmean < 0
    t_right = ((x1-x2)-(-popmean))/(sp*math.sqrt((1/n1)+(1/n2)))
    # if t_left > -1*crit_value:
    #     print('Do not reject Null')
    # else:
    #     print('Reject Null')
    # if t_right < crit_value:
    #     print('Do not reject Null')
    # else:
    #     print('Reject Null')
    return {'left t-stastic': t_left, 'right t-statistic': t_right, 'critical value': crit_value, 'reject null': t_left < -1*crit_value and t_right > crit_value}

# VERSION 1.0- performs (19*48 t-tests altogether and returns number of failed t-tests, 
# user is expected to use trial and error to get ideal popmean value)
# obtained value is the maximum value of interval across all hours for all yearly pairs

# # count of failed t-tests
# count = 0
# popmean = 0.01 # population mean difference

# for year in range(2004,2022):
#     # getting S.I. data for two consecutive years
#     tempdf = pd.read_excel(r"D:\Projects\ntu-vish\Seasonality Index Data\Half-Hourly S.I. per Month(Mon-Fri,Weekends).xlsx", sheet_name = str(year), index_col=0, header=[0,1])
#     tempdf2 = pd.read_excel(r"D:\Projects\ntu-vish\Seasonality Index Data\Half-Hourly S.I. per Month(Mon-Fri,Weekends).xlsx", sheet_name = str(year+1), index_col=0, header=[0,1])
#     # performing t-tests for all hours for a particular day of the week
#     for hour in tempdf.index:
#         sample1 = tempdf.loc[hour].xs('Fri',axis=0,level=1)
#         sample2 = tempdf2.loc[hour].xs('Fri',axis=0,level=1)
#         if not ttest(sample1,sample2,popmean)['reject null']:
#             count +=1
# print(f'Failed- {count}, PopMean- {popmean}')

# VERSION 2.0- performs individual t-tests for a particular hour and yearly-pair
# all possible combinations of yearly pairs for years between 2004 and 2022 are considered
# popmean values are calculated on their own and all the results are stored in an excel file with different sheets for weekdays and weekends data 

# for daytype in ['weekdays','weekends']:
#     dfdict = {} # for our dataframe (table) storing values
#     for i in range(2004,2022):
#         for j in range(i+1,2023):
#             tempdf = pd.read_excel(r"D:\Projects\ntu-vish\Seasonality Index Data\Hourly S.I. per Month(Weekdays,Weekends).xlsx", sheet_name = str(i), index_col=0, header=[0,1])
#             tempdf2 = pd.read_excel(r"D:\Projects\ntu-vish\Seasonality Index Data\Hourly S.I. per Month(Weekdays,Weekends).xlsx", sheet_name = str(j), index_col=0, header=[0,1])

#             dfdict[f'{i}-{j}'] = [] # list to hold all hours' t-test results for a particular year pair
#             for hour in tempdf.index:
#                 sample1 = tempdf.loc[hour].xs(daytype,axis=0,level=1)
#                 sample2 = tempdf2.loc[hour].xs(daytype,axis=0,level=1)
#                 # procedure to calculate popmean value for a particular hour
#                 popmean = 0.00 # population mean difference
#                 while True:
#                     count = 0
#                     if not ttest(sample1,sample2,popmean)['reject null']:
#                         count +=1
            
#                     if count:
#                         #print(f'Failed- {count}, PopMean- {popmean}')
#                         # update popmean
#                         popmean = round(popmean+0.001,3)
#                     else:
#                         # print(f'FINAL RESULTS!! Failed- {count}, PopMean- {popmean}, Hour- ',hour)
#                         break
#                 # adding hour values to the given yearly pair list
#                 dfdict[f'{i}-{j}'].append(popmean)
            
#     df = pd.DataFrame(dfdict,index=tempdf.index)

#     if daytype == 'weekdays':
#         df.to_excel('t-test results.xlsx', sheet_name=str(daytype))
#     else:
#         with pd.ExcelWriter('t-test results.xlsx', mode='a', engine='openpyxl') as writer:
#             df.to_excel(writer, sheet_name = str(daytype))

# VERSION 2.1- performs t-test for monthly seasonality data for all possible yearly pairs

df = pd.DataFrame(columns = [f'{i}-{j}' for i in range(2004,2022) for j in range(i+1,2023) ])

for daytype in ['weekdays','weekends']:
    tempdf = pd.read_excel(r"D:\Projects\ntu-vish\Seasonality Index Data\S.I. Month of The Year [Corrected].xlsx", sheet_name = str(daytype), index_col=0) # loads monthly seasonality data into a temporary dataframe for weekdays/weekends
    dfdict = {} # for our dataframe (table) storing values
    for i in range(2004,2022):
        for j in range(i+1,2023):
            # 2 year columns
            sample1 = tempdf[str(i)]
            sample2 = tempdf[str(j)]
            # procedure to calculate popmean value
            popmean = 0.00 # population mean difference
            while True:
                count = 0
                if not ttest(sample1,sample2,popmean)['reject null']:
                    count +=1
        
                if count:
                    #print(f'Failed- {count}, PopMean- {popmean}')
                    # update popmean
                    popmean = round(popmean+0.001,3)
                else:
                    # print(f'FINAL RESULTS!! Failed- {count}, PopMean- {popmean}, Hour- ',hour)
                    break
            # a row entry for weekdays/weekends to the dataframe
            dfdict[f'{i}-{j}'] = popmean
    df.loc[daytype] =  dfdict

df.transpose().to_excel('Monthly S.I. t-test results.xlsx')