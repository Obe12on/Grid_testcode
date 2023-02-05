import pmdarima as pm
import pandas as pd
import matplotlib.pyplot as plt

class callArima:
    def train(dataDict : dict ) -> pd.DataFrame:
        model = pm.auto_arima(dataDict['Sales_data'], m = 12, seasonal = True,
            start_p = 0, start_q = 0, max_order = 4, error_action = 'ignore',
            supress_warnings = True,test = 'adf', stepwise = True, trace = True, 
            X = dataDict['Discount_data'])
        forecast = model.predict(n_periods = 14, return_conf_int = True, X = dataDict['Discount_forecast'])
        forecast_result = pd.DataFrame(forecast[0], columns =['Prediction'])
        return forecast_result.iloc[2:]
        

if __name__ == '__main__':
    callArima()