import pandas as pd
from sklearn.linear_model import LinearRegression

popgrowth = pd.read_excel("Population Growth.xlsx", index_col=0)
demandgdp = pd.read_excel("Total Yearly Demand.xlsx", index_col=0)
demandgdp.columns = ['demand','gdp']
demandgdp['popgrowth'] = popgrowth['Total Population ']

testseries = pd.read_excel('testseries.xlsx', index_col=0)

with open('i_sh.txt', 'r') as file:
    i_sh = [float(line.strip()) for line in file] # hourly SIs for weekdays

with open('i_sm.txt', 'r') as file:
    i_sm = [float(line.strip()) for line in file]  # monthly SIs for first cycle

# 1. GDP PopGrowth Model
X_fit, y_fit = demandgdp[['gdp','popgrowth']].loc[2004:2017], demandgdp.loc[2004:2017].demand
linreg = LinearRegression()
linreg.fit(X_fit.values,y_fit.values)

forecast2018yearly = int(linreg.predict([demandgdp[['gdp','popgrowth']].loc[2018].values]))
forecasted = [forecast2018yearly * i_sh[i%(24*7)] * i_sm[i] /(365*24) for i in range(365*24)]

pd.DataFrame({'Original 2018': list(testseries.iloc[:365*24].value), 'Forecast 2018': forecasted}, index=testseries.index[:365*24]).to_excel('GDP-PopGrowthModel[Forecast 2018].xlsx')

# 2. PopGrowth Model
X_fit, y_fit = demandgdp.loc[2004:2017].popgrowth, demandgdp.loc[2004:2017].demand
poplinreg = LinearRegression()
poplinreg.fit(X_fit.values.reshape(-1,1),y_fit.values.reshape(-1,1))

forecast2018yearly = int(poplinreg.predict([[demandgdp.loc[2018].popgrowth]]))
forecasted = [forecast2018yearly * i_sh[i%(24*7)] * i_sm[i] /(365*24) for i in range(365*24)]

pd.DataFrame({'Original 2018': list(testseries.iloc[:365*24].value), 'Forecast 2018': forecasted}, index=testseries.index[:365*24]).to_excel('PopGrowthModel[Forecast 2018].xlsx')