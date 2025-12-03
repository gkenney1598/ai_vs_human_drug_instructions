import csv
import pandas as pd

with open('data/editinghumangenerated.csv', newline='', encoding='utf-8') as f:
    df = pd.read_csv(f)
    for row in df.iterrows():
        text = row[1]["text"]
        loc = text.find("What should I know about storage and disposal of this medication?") #if you experience a serious side effect
        row[1]["text"] = text[:loc]
        
df.to_csv('data/editinghumangenerated.csv', index=False, encoding='utf-8')

