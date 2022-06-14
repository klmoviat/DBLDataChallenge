import sqlite3
import pandas as pd
import json

data = [json.loads(line) for line in open('airlines4.json', 'r')]

df = pd.DataFrame(data)
print(df.head())
print(df.columns)

#data.to_sql('KLM_db')
#conn = sqlite3.connect('data.db')
#cursor = conn.cursor()

#conn = sqlite3.connect('test_database')
#c = conn.cursor()

#c.execute('CREATE TABLE IF NOT EXISTS products (product_name text, price number)')
#conn.commit()
#df.to_sql('products', conn, if_exists='replace', index = False)

#%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults
plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

# hide FutureWarnings, which may show for Seaborn calls in most recent Anaconda
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

ax = df['lang'].plot();
ax.get_figure().savefig('lang.pdf')
