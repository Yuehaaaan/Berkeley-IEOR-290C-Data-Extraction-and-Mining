import pandas as pd
from pandas import Series
import pylab as plt
dg=pd.read_csv('loans.csv',delimiter=',')
dh=dg['category'].value_counts()[:10]
dh.plot(kind='bar')
