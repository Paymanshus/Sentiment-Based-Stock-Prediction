import re
import os
import pandas as pd

dates = {}

for file in os.listdir('text'):
    if file.endswith('.txt'):
        dt = re.findall(
            r'\d{2}_\d{1}_\d{2}|\d{1}_\d{2}_\d{2}|\d{1}_\d{1}_\d{2}', file)
        if not not dt:
            dates[file] = dt

dates_df = pd.DataFrame(dates).T
dates_df.to_csv('dates.csv')
