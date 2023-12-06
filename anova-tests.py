import pandas as pd
import scipy.stats as stats

start_year = 2005
end_year = 2007
#hours = ['01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '00:00']
#hours = ['02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00']
#hours = ['03:00', '06:00', '09:00', '12:00', '15:00','18:00', '21:00', '00:00']
#hours = ['04:00', '08:00', '12:00', '16:00', '20:00', '00:00']
types = ['weekdays', 'weekends']

while end_year < 2023:
    year_col1 = []
    year_col2 = []
    type_col = []
    hour_col = []
    fvalue_col = []
    pvalue_col = []
    slevel_col = []
    conclusion = []
    for daytype in types:
        for hour in hours:
            year_list = []
            for i in range(start_year,end_year+1):
                tempdf = pd.read_excel('D:/Projects/ntu-vish/Seasonality Index Data/Hourly S.I. per Month(Weekdays,Weekends).xlsx', sheet_name = str(i), index_col=0, header=[0,1])
                year_list.append(tempdf.loc[hour].xs(daytype,axis=0,level=1))
            testdf = pd.concat(year_list, axis = 1)
            testdf.columns = [i for i in range(start_year,end_year+1)]

            fvalue, pvalue = stats.f_oneway(*[testdf[i] for i in testdf.columns])
            year_col1.append(start_year)
            year_col2.append(end_year)
            type_col.append(daytype)
            hour_col.append(hour)
            fvalue_col.append(fvalue)
            pvalue_col.append(pvalue)
            slevel_col.append(0.05)
            if pvalue > 0.05:
                conclusion.append('Do not reject')
            else:
                conclusion.append('Reject')
    df = pd.DataFrame(data = {
        'Start Year' : year_col1,
        'End Year' : year_col2,
        'Type' : type_col,
        'Hour' : hour_col,
        'f-value' : fvalue_col,
        'p-value' : pvalue_col,
        'significance level' : slevel_col,
        'Conclusion' : conclusion
        })
    if start_year == 2005:
        df.to_excel('Consolidated ANOVA [2 hour blocks].xlsx', index = False, sheet_name = '{}-{}'.format(start_year, end_year), float_format = '%.3f')
    else:
        with pd.ExcelWriter('Consolidated ANOVA [2 hour blocks].xlsx', mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, index = False, sheet_name = '{}-{}'.format(start_year, end_year), float_format = '%.3f')
    start_year += 3
    end_year += 3