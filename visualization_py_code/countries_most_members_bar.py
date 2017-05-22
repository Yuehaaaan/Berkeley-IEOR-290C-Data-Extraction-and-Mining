import pandas as pd
from pandas import Series
import pylab as plt
df=pd.read_csv('members_city_state_country',delimiter=',')
s_country=df['country']
s1=s_country.value_counts()[:10]
s1.plot(kind='bar')
plt.ylabel('number of members')
plt.xlabel('countries')
plt.title('countries that have most members')
plt.show()

