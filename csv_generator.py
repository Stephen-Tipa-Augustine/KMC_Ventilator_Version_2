import math
import time

import pandas as pd


print('generating files...')
t = 0

while True:
    data = {}
    data['time'] = [t]
    data['pressure'] = [math.cos(t)]
    data['flow'] = [math.sin(t)]
    data['volume'] = [1/math.cos(t)]

    df = pd.DataFrame(data)
    print('generating csv files')
    try:
        df2 = pd.read_csv('rt_data.csv')
    except:
        df2 = None
    if df2 is not None:
        df = df2.append(df, ignore_index=True)
    df.to_csv('rt_data.csv', index=False)
    time.sleep(.05)
    print("wrote to file successfully")
    t += 1