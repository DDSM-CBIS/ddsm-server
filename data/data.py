import re
import pandas as pd
import json

def to_camel_case(column_name):
    components = re.split(r'[_ ]', column_name)
    return components[0].lower() + ''.join(x.title() for x in components[1:])

def rename_columns_to_camel_case(df):
    new_columns = {col: to_camel_case(col) for col in df.columns}
    return df.rename(columns=new_columns)

def extract_unique_values(columns_to_extract):
    unique_values = {col: set() for col in columns_to_extract}
    
    for col in columns_to_extract:
        if col in calc_df.columns:
            unique_values[col].update(calc_df[col].dropna().unique())
    
    for col in columns_to_extract:
        if col in mass_df.columns:
            unique_values[col].update(mass_df[col].dropna().unique())
    
    unique_values = {k: list(v) for k, v in unique_values.items()}
    
    return unique_values

calc_df = pd.read_csv("./data/calc_set.csv")
calc_df = rename_columns_to_camel_case(calc_df)
mass_df = pd.read_csv("./data/mass_set.csv")
mass_df = rename_columns_to_camel_case(mass_df)
series_df = pd.read_csv("data/getSeries.csv")