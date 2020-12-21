import pandas as pd
import os
from pprint import pprint

dict = {}

for file in os.listdir('text'):
    if(file.endswith('.txt')):
        f = open('text/' + file, 'r')
        text = f.read()
        dict[file] = text

pprint(dict)


df = pd.DataFrame(dict.items())
print(df)
df.to_csv('saved_text.csv')
