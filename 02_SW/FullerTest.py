import pandas as pd
from statsmodels.tsa.stattools import adfuller

class Dickey_Fuller:
    def isStationary(data : 'pd.core.frame.DataFrame') -> bool:
        
        adft = adfuller(data)
        if adft[1] < 0.05 and adft[0] < adft[4]['1%'] and adft[0] < adft[4]['5%'] and adft[0] < adft[4]['10%'] :
            result = True
        else:
            result = False
        return result

if __name__ == '__main__':
    Dickey_Fuller()