import re
import pandas as pd
from data.data import calc_df, mass_df

def to_camel_case(column_name):
    components = re.split(r'[_ ]', column_name)
    return components[0].lower() + ''.join(x.title() for x in components[1:])

def rename_columns_to_camel_case(df):
    new_columns = {col: to_camel_case(col) for col in df.columns}
    return df.rename(columns=new_columns)

def extract_unique_values(columns_to_extract):
    unique_values = {col: set() for col in columns_to_extract}
    
    for col in columns_to_extract:
        if col in calcDf.columns:
            unique_values[col].update(calcDf[col].dropna().unique())
    
    for col in columns_to_extract:
        if col in massDf.columns:
            unique_values[col].update(massDf[col].dropna().unique())
    
    unique_values = {k: list(v) for k, v in unique_values.items()}
    
    return unique_values

def get_common_columns():
    common_columns = set(calc_df.columns).intersection(set(mass_df.columns))
    renamed_columns = [to_camel_case(col) for col in common_columns if "file path" not in col]
    return renamed_columns

def get_distinct_columns():
    distinct_columns = set(calc_df.columns).symmetric_difference(set(mass_df.columns))
    renamed_columns = [to_camel_case(col) for col in distinct_columns]
    return renamed_columns

calcDf = rename_columns_to_camel_case(calc_df)
massDf = rename_columns_to_camel_case(mass_df)
