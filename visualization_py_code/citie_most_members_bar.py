import pandas as pd
from pandas import Series
import pylab as plt
df=pd.read_csv('members_city_state_country',delimiter=',')
s_cities=df['city']
s1=s_cities.value_counts()[:10]
s1.plot(kind='bar')
plt.ylabel('number of members')
plt.xlabel('cities')
plt.title('cities that have most members')
plt.show()
