## Current Model(s)-  

### *Model 1: Constant Seasonality Model [Unknown Demand]*

$L_0$ = Mean of first year input  
$T_0$ = 0  
$\alpha$ = 0.19, 
$\beta$ = 0.88  [Obtained for 2011-2017 train data and 2018 test data for the least MAPE]  
S.I. indices = Mean of S.I. indices for 2011-2017

We update the values of $L_t$ and $T_t$ for the input data at each step (each hour) as follows:

$L_t = L_{t-1} + B_{t-1} + \alpha\left(\frac{D_t}{S_{t-m_h}^{h}S_{t-m_d}^{d}S_{t-m_m}^{m}} - (L_{t-1} + B_{t-1}) \right)$


$B_t = B_{t-1} + \beta(L_t - L_{t-1} - B_{t-1})$

We stop updating the values of $L_t$ and $T_t$ and forecast the values for the future steps (hourly data for next year) as follows:

$F_{t+1} = (L_t + B_t)(S_{t-m_h}^{h}S_{t-m_d}^{d}S_{t-m_m}^{m})$


### *Model 2: Constant Seasonality Model [Known Demand]*

Same as previous model, but we keep updating the values of $L_t$ and $T_t$ at each step (each hour) for the forecast year data too.  

**Note: We use only previous 5 years of data as input to forecast next year data**

### *Code:*

```python
for t in range(len(series) + future_steps):
    if t>= len(series):
        forecast_t = (l_t1 + t_t1) * (i_sh[t%24*7] * i_sm[t%365*24])
        forecast.append(forecast_t)
    else:
        # updating L_t,B_t values
        l_t = (l_t1 + t_t1) + alpha * ((series.iloc[t]/(i_sh[t%24*7] * i_sm[t%365*24])) - (l_t1 + t_t1))
        t_t1 = t_t1 + beta * (l_t - l_t1 - t_t1)
        l_t1 = l_t # l_t is l_t-1 now for the next period

        forecast.append((l_t1 + t_t1) * (i_sh[t%24*7] * i_sm[t%365*24]))
```

## Revised Model-  

- We only employ the unknown demand model. We use the same values of $\alpha$ and $\beta$ as before. We use the same values of $L_0$ and $T_0$ as before.   
- We use the last year's data for S.I. indices. 
- We update the values of $L_t$ and $T_t$ for the input data after each 24 steps (each day) only.

### *Code:*

```python
for t in range(len(series) + future_steps):
    if t>= len(series):
        forecast_t = (l_t1 + t_t1) * (i_sh[t%24*7] * i_sm[t%365*24])
        forecast.append(forecast_t)
    else:
        if t%24 == 0:
            # updating L_t,B_t values
            l_t = (l_t1 + t_t1) + alpha * ((series.iloc[t]/(i_sh[t%24*7] * i_sm[t%365*24])) - (l_t1 + t_t1))
            t_t1 = t_t1 + beta * (l_t - l_t1 - t_t1)
            l_t1 = l_t # l_t is l_t-1 now for the next period

        forecast.append((l_t1 + t_t1) * (i_sh[t%24*7] * i_sm[t%365*24]))
```