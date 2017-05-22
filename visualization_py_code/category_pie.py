import pandas as pd
from pandas import Series
import pylab as plt
dg=pd.read_csv('loans.csv',delimiter=',')
dh=dg['category'].value_counts()[:10]
dh.plot(kind='pie',colors=['brown','pink','maroon','cyan','red','green','blue','yellow','purple','orange'],autopct='%.2f')
plt.show()