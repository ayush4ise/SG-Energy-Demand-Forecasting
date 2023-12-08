import pandas as pd
from scipy.stats import ttest_1samp

popmean = 0.005
for year in range(2004,2022):
    hour_col = []
    tstat = []
    pval = []
    conc = []

    tempdf = pd.read_excel('D:/Projects/ntu-vish/Seasonality Index Data/Hourly S.I. per Month(Weekdays,Weekends).xlsx', sheet_name = str(year), index_col=0, header=[0,1])
    tempdf2 = pd.read_excel('D:/Projects/ntu-vish/Seasonality Index Data/Hourly S.I. per Month(Weekdays,Weekends).xlsx', sheet_name = str(year+1), index_col=0, header=[0,1])
    
    for hour in tempdf.index:
        res = ttest_1samp(abs(tempdf.loc[hour].xs('weekdays',axis=0,level=1)-tempdf2.loc[hour].xs('weekdays',axis=0,level=1)), popmean = popmean)
        hour_col.append(hour)
        tstat.append(res.statistic)
        pval.append(res.pvalue)
        if res.pvalue > 0.05:
            conc.append('Do not reject')
        else: conc.append('Reject')
    df = pd.DataFrame(data = {
    'Hour' : hour_col,
    't-stat' : tstat,
    'p-value' : pval,
    'Conclusion' : conc
    })
    if year == 2004:
            df.to_excel('Consolidated t-test results [weekdays].xlsx', index = False, sheet_name = '{}-{}'.format(year, year+1), float_format = '%.3f')
    else:
        with pd.ExcelWriter('Consolidated t-test results [weekdays].xlsx', mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, index = False, sheet_name = '{}-{}'.format(year, year+1), float_format = '%.3f')