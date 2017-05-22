import pandas as pd
from pandas import Series
import pylab as plt
dg=pd.read_csv('loan_country_total_amount',delimiter=',')
s = dg["country_total_amount"]
s.index = dg["top_countries"]
s1 = s.copy()
s1.sort(ascending=False)
s1.plot(kind='bar')
plt.show()
