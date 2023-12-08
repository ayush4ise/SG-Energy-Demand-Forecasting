from models import *
from utils_ts import *

import pandas as pd
import numpy as np

def ESInput():
    # alpha, beta, period_m, future_steps, i_sh, i_sm
    alpha = 0.19
    beta = 0.88
    period_m = [24*7, 365*24]
    future_steps = 365*24
    with open('input/i_sh[unscaled].txt', 'r') as file:
        i_sh = [float(line.strip()) for line in file] # hourly SIs for weekdays

    with open('input/i_sm.txt', 'r') as file:
        i_sm = [float(line.strip()) for line in file]  # monthly SIs for first cycle

    return alpha, beta, period_m, future_steps, i_sh, i_sm

def ESPipeline(forecast_year:int, known_demand = 'unknown'):
    # known_demand = ['known','unknown']
    inputseries = timeseries(2011,forecast_year, 'system')
    testseries = timeseries(forecast_year,forecast_year, 'system')
    if known_demand == 'unknown':
        forecast = constant_seasonality_model(inputseries[inputseries.index.year != forecast_year], *ESInput())
    elif known_demand == 'known':
        forecast = constant_seasonality_known_demand_model(inputseries,*ESInput())
    forecastdf = pd.DataFrame({f'Actual {forecast_year}': list(testseries.value)[:365*24], f'Forecast {forecast_year}': [float(i) for i in forecast[-365*24:]]}, index=testseries.index[:365*24])
    forecastdf.to_excel(f'System_ES_{known_demand.capitalize()}Demand{forecast_year}.xlsx')
    
    return forecastdf

def LinRegInput():
    import pandas as pd

    popgrowth = pd.read_excel("input/Population Growth.xlsx", index_col=0)
    demandgdp = pd.read_excel("input/Total Yearly Demand.xlsx", index_col=0)
    demandgdp.columns = ['demand','gdp']
    demandgdp['popgrowth'] = popgrowth['Total Population ']

    with open('input/i_sh[unscaled].txt', 'r') as file:
        i_sh = [float(line.strip()) for line in file] # hourly SIs for weekdays

    with open('input/i_sm.txt', 'r') as file:
        i_sm = [float(line.strip()) for line in file]  # monthly SIs for first cycle
    
    return demandgdp, i_sh, i_sm

class LinRegPipelines():
    def __init__(self, forecast_year, demandgdp, i_sh, i_sm):
        self.forecast_year = forecast_year
        self.demandgdp = demandgdp
        self.i_sh = i_sh
        self.i_sm = i_sm
        self.testseries = timeseries(forecast_year,forecast_year,'system')

    def gdp_model(self):
        from sklearn.linear_model import LinearRegression
        X_fit, y_fit = self.demandgdp.loc[2004:self.forecast_year-1].gdp, self.demandgdp.loc[2004:self.forecast_year-1].demand
        gdplinreg = LinearRegression()
        gdplinreg.fit(X_fit.values.reshape(-1,1),y_fit.values.reshape(-1,1))

        gdpforecastyearly = int(gdplinreg.predict([[self.demandgdp.loc[self.forecast_year].gdp]]))
        gdpforecasted = [gdpforecastyearly * self.i_sh[i%(24*7)] * self.i_sm[i] /(365*24) for i in range(365*24)]

        forecastdf = pd.DataFrame({'Actual': list(self.testseries.value)[:365*24], 'Forecast': gdpforecasted}, index=self.testseries.index[:365*24])
        forecastdf.to_excel(f'System_GDPModel_{self.forecast_year}.xlsx')

        return forecastdf

    def gdppop_model(self):
        from sklearn.linear_model import LinearRegression
        X_fit, y_fit = self.demandgdp[['gdp','popgrowth']].loc[2004:self.forecast_year-1], self.demandgdp.loc[2004:self.forecast_year-1].demand
        gpoplinreg = LinearRegression()
        gpoplinreg.fit(X_fit.values,y_fit.values)

        gpopforecastyearly = int(gpoplinreg.predict([self.demandgdp[['gdp','popgrowth']].loc[2018].values]))
        gpopforecasted = [gpopforecastyearly * self.i_sh[i%(24*7)] * self.i_sm[i] /(365*24) for i in range(365*24)]

        forecastdf = pd.DataFrame({'Actual': list(self.testseries.value)[:365*24], 'Forecast': gpopforecasted}, index=self.testseries.index[:365*24])
        forecastdf.to_excel(f'System_GDPPopModel_{self.forecast_year}.xlsx')

        return forecastdf
    
    def pop_model(self):
        from sklearn.linear_model import LinearRegression
        X_fit, y_fit = self.demandgdp.loc[2004:self.forecast_year-1].popgrowth, self.demandgdp.loc[2004:self.forecast_year-1].demand
        poplinreg = LinearRegression()
        poplinreg.fit(X_fit.values.reshape(-1,1),y_fit.values.reshape(-1,1))

        popforecastyearly = int(poplinreg.predict([[self.demandgdp.loc[2018].popgrowth]]))
        popforecasted = [popforecastyearly * self.i_sh[i%(24*7)] * self.i_sm[i] /(365*24) for i in range(365*24)]

        forecastdf = pd.DataFrame({'Actual': list(self.testseries.value)[:365*24], 'Forecast': popforecasted}, index=self.testseries.index[:365*24])
        forecastdf.to_excel(f'System_Pop_Model_{self.forecast_year}.xlsx')

        return forecastdf
    
def ProphetPipeline(forecast_year:int):
    from prophet import Prophet
    inputseries = timeseries(2011,forecast_year-1, demandtype='system')
    testseries = timeseries(forecast_year,forecast_year, demandtype='system')
    inputseries.reset_index(inplace=True)
    inputseries.columns = ['ds','y']
    model = Prophet()
    model.fit(inputseries)

    future = model.make_future_dataframe(periods=365*24, freq='H')
    fcst = model.predict(future)
    forecastdf = pd.DataFrame({'Actual': list(testseries.value)[:365*24], 'Forecast': list(fcst['yhat'][-365*24:])}, index=testseries.index[:365*24])
    forecastdf.to_excel(f'System_Prophet_{forecast_year}.xlsx')

    return forecastdf

def SARIMAXPipeline(forecast_year:int):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    inputseries = timeseries(2011,forecast_year-1, demandtype='system')
    testseries = timeseries(forecast_year,forecast_year, demandtype='system')
    
    # Define SARIMAX model with appropriate seasonal orders (24 for daily, 7 for weekly, 30 for monthly)
    sarimax_model = SARIMAX(inputseries, order=(1, 0, 1), seasonal_order=(1, 0, 1, 24), 
                        enforce_stationarity=False, enforce_invertibility=False)
    sarimax_results = sarimax_model.fit()

    # Forecast
    forecast_steps = len(testseries)
    forecast = sarimax_results.get_forecast(steps=forecast_steps)

    forecastdf = pd.DataFrame({'Actual': list(testseries.value), 'Forecast': list(forecast.predicted_mean)}, index=testseries.index)
    forecastdf.to_excel(f'System_SARIMAX_{forecast_year}.xlsx')

    return forecastdf

def MSTLARIMAPipeline(forecast_year:int):
    from statsforecast import StatsForecast
    from statsforecast.models import MSTL, AutoARIMA
    inputseries = timeseries(2011,forecast_year-1, demandtype='system')
    testseries = timeseries(forecast_year,forecast_year, demandtype='system')

    df = inputseries.copy()
    df.reset_index(inplace=True)
    df.columns = ['ds','y']
    df.insert(0, 'unique_id', 'SED_Load_hourly')
    df = df.sort_values(['unique_id', 'ds']).reset_index(drop=True)

    models = [MSTL(
    season_length=[24, 24 * 7, 365 * 24], # seasonalities of the time series 
    trend_forecaster=AutoARIMA() # model used to forecast trend
    )]

    sf = StatsForecast(
        models=models, # model used to fit each time series 
        freq='H', # frequency of the data
    )

    sf = sf.fit(df=df)
    forecast = sf.predict(h=len(testseries))

    forecastdf = pd.DataFrame({'Actual': list(testseries.value), 'Forecast': list(forecast['MSTL'])}, index=testseries.index)
    forecastdf.to_excel(f'System_MSTLARIMA_{forecast_year}.xlsx')
    return forecastdf

def DHRPipeline(forecast_year:int):
    from prophet import Prophet
    inputseries = timeseries(2011,forecast_year-1, demandtype='system')
    testseries = timeseries(forecast_year,forecast_year, demandtype='system')
    inputseries.reset_index(inplace=True)
    inputseries.columns = ['ds','y']

    model = Prophet(seasonality_mode='multiplicative', yearly_seasonality=False)
    model.add_seasonality(name='hourly', period=24, fourier_order=8)
    model.add_seasonality(name='weekly', period=7, fourier_order=3)
    model.add_seasonality(name='monthly', period=30.44, fourier_order=5)

    model.fit(inputseries)

    future = model.make_future_dataframe(periods=365*24, freq='H')
    fcst = model.predict(future)
    forecastdf = pd.DataFrame({'Actual': list(testseries.value)[:365*24], 'Forecast': list(fcst['yhat'][-365*24:])}, index=testseries.index[:365*24])
    forecastdf.to_excel(f'System_DHR_{forecast_year}.xlsx')

    return forecastdf