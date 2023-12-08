import pandas as pd
from sklearn.linear_model import LinearRegression

demandgdp = pd.read_excel("Total Yearly Demand.xlsx", index_col=0)
demandgdp.columns = ['demand','gdp']

testseries = pd.read_excel('testseries.xlsx', index_col=0)
with open('i_sh.txt', 'r') as file:
    i_sh = [float(line.strip()) for line in file] # hourly SIs for weekdays

with open('i_sm.txt', 'r') as file:
    i_sm = [float(line.strip()) for line in file]  # monthly SIs for first cycle

X_fit, y_fit = demandgdp.loc[2004:2017].gdp, demandgdp.loc[2004:2017].demand
linreg = LinearRegression()
linreg.fit(X_fit.values.reshape(-1,1),y_fit.values.reshape(-1,1))

forecast2018yearly = int(linreg.predict([[demandgdp.loc[2018].gdp]]))
forecasted = [forecast2018yearly * i_sh[i%(24*7)] * i_sm[i] /(365*24) for i in range(365*24)]

pd.DataFrame({'Original 2018': list(testseries.iloc[:365*24].value), 'Forecast 2018': forecasted}, index=testseries.index[:365*24]).to_excel('GDPModel[Forecast 2018].xlsx')