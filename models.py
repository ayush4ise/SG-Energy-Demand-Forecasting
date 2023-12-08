def constant_seasonality_model(series,
          alpha:float,
          beta:float,
          period_m:list,
          future_steps:int,
          i_sh:list,
          i_sm:list): # future_steps = how many periods to forecast
    """
    alpha, beta - parameters used in Holt's Winter Technique

    period_m = [24*7, 365*24] hourly, monthly seasonalities

    future_steps = forecast periods after input series

    i_sh = hourly seasonality for each weekdays (list of length- 24*7)

    i_sm = monthly seasonality (list of length- 365*24)
    """

    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")

    i_l = [np.mean(series.iloc[0:period_m[-1]])] # Initial level
    i_t = [0] # Initial trend

    forecast = [] # can change it to numpy array to have forecast dates as indices
    for t in range(len(series) + future_steps):
        if t>= len(series):
                forecast_t = (i_l[-1] + i_t[-1]) * (i_sh[t%period_m[0]] * i_sm[t%period_m[1]])
                forecast.append(forecast_t)
        else:
                # updating L_t,B_t values
                l_t = (i_l[-1] + i_t[-1]) + alpha * ((series.iloc[t]/(i_sh[t%period_m[0]] * i_sm[t%period_m[1]])) - (i_l[-1] + i_t[-1]))
                i_t[-1] = i_t[-1] + beta * (l_t - i_l[-1] - i_t[-1])
                i_l[-1] = l_t # l_t is l_t-1 now for the next period

                forecast.append((i_l[-1] + i_t[-1]) * (i_sh[t%period_m[0]] * i_sm[t%period_m[1]]))

    return forecast

def constant_seasonality_known_demand_model(series,
          alpha:float,
          beta:float,
          period_m:list,
          future_steps:int,
          i_sh:list,
          i_sm:list): # future_steps = how many periods to forecast
    """
    alpha, beta - parameters used in Holt's Winter Technique

    period_m = [24*7, 365*24] hourly, monthly seasonalities

    future_steps = forecast periods included at the end of input series

    i_sh = hourly seasonality for each weekdays (list of length- 24*7)

    i_sm = monthly seasonality (list of length- 365*24)
    """

    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")

    i_l = [np.mean(series.iloc[0:period_m[-1]])] # Initial level
    i_t = [0] # Initial trend

    forecast = [] # can change it to numpy array to have forecast dates as indices
    for t in range(len(series)):
        # updating L_t,B_t values
        l_t = (i_l[-1] + i_t[-1]) + alpha * ((series.iloc[t]/(i_sh[t%period_m[0]] * i_sm[t%period_m[1]])) - (i_l[-1] + i_t[-1]))
        i_t[-1] = i_t[-1] + beta * (l_t - i_l[-1] - i_t[-1])
        i_l[-1] = l_t # l_t is l_t-1 now for the next period

        forecast.append((i_l[-1] + i_t[-1]) * (i_sh[t%period_m[0]] * i_sm[t%period_m[1]]))

    return forecast