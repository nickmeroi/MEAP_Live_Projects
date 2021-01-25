import pandas as pd
import numpy as np
import re
from pprint import pprint


def import_data(address):

    data = pd.read_html(address)

    # our target table has no caption so we can't use match in read_hmtl.
    # instead we scan the df columns and select the df with matching columns
    # if no suitable df has been found an empty df is returned

    for df in data:
        if df.columns.values.tolist() == ['Year', 'Result', 'Host arena', 'Host city', 'Game MVP']:
            return df
        else:
            continue


def clean_raw_data(df):

    df.set_index("Year", inplace=True)
    df.drop(["Game MVP", "Host arena"], axis=1, inplace=True)
    df["Host city"] = df["Host city"].str.split(",").str[0]
    df['Host city'].dropna(axis=0, how="any", inplace=True)
    df["East"] = df["Result"].str.extract(r'(?:East )(\d+)', expand=False).astype('float')
    df["West"] = df["Result"].str.extract(r'(?:West )(\d+)', expand=False).astype('float')

    return df

def get_counts(df):

    df["Diff"] = abs(df["East"] - df["West"])
    df = df.groupby(['Diff'])['Diff'].count().sort_index(ascending=False)


    return df

def get_counts_2(df):

    df = df.groupby(['Host city']).agg(East=pd.NamedAgg(column='East', aggfunc=pd.Series.mean),
                                        West=pd.NamedAgg(column='West', aggfunc=pd.Series.mean),
                                        Count=pd.NamedAgg(column='Host city', aggfunc='count'))

    return df[df['Count'] > 1].sort_values(by='Count')

def main():

    web_page = 'https://en.wikipedia.org/wiki/NBA_All-Star_Game'
    raw_data = import_data(web_page)

    if not raw_data.empty:
        clean_data = clean_raw_data(raw_data)
        #pprint(clean_data)

    if not clean_data.empty:
        counts = get_counts(clean_data)
        pprint(get_counts(clean_data))

        counts_2 = get_counts_2(clean_data)
        pprint(get_counts_2(clean_data))


if __name__ == '__main__':
    main()
