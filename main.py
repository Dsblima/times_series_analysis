import warnings
import itertools
import os
import os.path
import numpy as np
from scipy.stats import variation
from scipy.stats import kurtosis
from scipy.stats import shapiro
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss

import matplotlib
from pylab import rcParams
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

path = "data/"
stationarityDefinitionlist = []
def kpss_test(series, **kw):    
    statistic, p_value, n_lags, critical_values = kpss(series, **kw)
    # Format Output
    print(f'KPSS Statistic: {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critial Values:')
    
    for key, value in critical_values.items():
        print(f'   {key} : {value}')
    
    result = f'Result: The series is {"not " if p_value < 0.05 else ""}stationary'
    print(result)    
    return result
    
def adfuller_test(series):
    result = adfuller(series)
    print(result)
    statistic, p_value, n_lags, critical_values = result[0], result[1], result[2], result[4]
    print(f'ADF Statistic:  {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critical Values:')
    for key, value in critical_values.items():
        print('\t%s: %.3f' % (key, value))
    result = f'Result: The series is {"not " if p_value > 0.05 else ""}stationary'     
    print(result)
    return result

def getModeToCreateFile(fileName):
    if not os.path.exists(fileName):
        return 'w'
    else:
        return 'a'
        
def shapiroTest(serie):
    alpha = 0.05
    stat, p = shapiro(serie)
    if p > alpha:
        return 'A série vem de uma distribuição normal.'
    else:
        return 'A série não vem de uma distribuição normal.'    
        
if __name__ == '__main__':
    fileName = 'stationarityDefinitionlist.txt'
    readMode = getModeToCreateFile(fileName)
    file = open(fileName, 'w')
        
    bases = ["Lynx", "Exchange Rate", "Yearly Sunspot",'Colorado River', 'Lake Erie', "airlines2", "Daily Female Births Dataset", 'Eletric', 'Gas',
             'Pollution', 'redwine']
    
    for base in bases:
        series = pd.read_csv(path + base + ".txt")
        print(base)
        y = series
        X = series.values        
        # print(y)
        cv =  variation(X, axis=0)*100
        curtose = kurtosis(X)
        p25 = np.percentile(X, 25)
        p75 = np.percentile(X,75)
        result = shapiroTest(y)        
                
        file.writelines(base + '\n')
        file.writelines("ADF Test: " + adfuller_test(X) + '\n')        
        file.writelines("KPSS Test: " + kpss_test(series) + '\n')
        file.writelines(result)
        file.writelines("CV " + str(cv) + '\n')
        file.writelines("Curtose " + str(curtose) + '\n')
        file.writelines("1 quartil " + str(p25) + '\n')
        file.writelines("3 quartil " + str(p75) + '\n')
        file.writelines('\n')

        # y.plot(figsize=(15, 6))
        # plt.show()

        # rcParams['figure.figsize'] = 18, 8
        # decomposition = sm.tsa.seasonal_decompose(y, model='additive', period=10)
        # # fig = decomposition.plot()
        # plt.show()
        # plt.savefig()


