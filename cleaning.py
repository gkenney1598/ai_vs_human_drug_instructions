import pandas as pd

def clean(name):
    with open(name, newline='', encoding='utf-8') as f:
        df = pd.read_csv(f)
        for row in df.iterrows():
            text = row[1]["text"]
            loc = text.find("") #insert text to be deleted
            row[1]["text"] = text[:loc]
            
    df.to_csv(name, index=False, encoding='utf-8')

def main():
    clean("<file_name>")

main()