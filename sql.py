import sqlite3
import numpy as np
import pandas as pd

import json

with open('airlines-1558611772040.json') as json_data:
    d = json.load(json_data)
    print(d)

#from pandas.io.json import json_normalize
#json_normalize(json_data)

#import json
#tweets = []
#for line in open('airlines-1558611772040.json', 'r'):
#    tweets.append(json.loads(line))