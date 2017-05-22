import pandas as pd
from pandas import Series
import pylab as plt
df = pd.read_csv('impact.csv',delimiter=',')
female = df['borrower_female_count'].sum()
male = df['borrower_male_count'].sum()
s = Series([female,male], index =['female','male'])
s.plot(kind='pie',colors=['brown','pink'],autopct='%.2f')
plt.show()
