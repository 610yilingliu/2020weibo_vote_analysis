# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# %%
def extract_time(time_str):
    """
    Extract time from file name
    """
    start = time_str.find('-')
    end = time_str.find('.csv')
    time_str = time_str[start + 1:end]
    time = time_str.split('_')
    y, m, d, h, mi = time
    formattted = y + '.' + m + '.' + d + ' ' + h + ':' + mi
    return formattted


# %%
def csv_creater(path):
    files = os.listdir(path)
    names_set = set()
    output_df = pd.DataFrame(columns = ["name"])
    for f in files:
        cur_time = extract_time(f)
        output_df[cur_time] = 0
        df = pd.read_csv(path + '/' + f)
        existed_names = output_df.index.values
        for row in df.iterrows():
            name = row[1]["name"]
            vote = int(row[1]["vote"])
            if name not in existed_names:
                print(name)
                output_df.loc[name] = 0
            output_df.loc[name, cur_time] = vote
    return output_df


# %%
csv_creater("./get_data/2020_data")


# %%



