import pandas as pd

def get_df(file_path):
    file = pd.read_csv(file_path)
    renamed_columns = {col: col.replace("_", " ") for col in file.columns}
    return file.rename(columns=renamed_columns)

calc_file_path = './data/calc_set.csv'
mass_file_path = './data/mass_set.csv'
series_file_path = './data/getSeries.csv'

calc_df = get_df(calc_file_path)
mass_df = get_df(mass_file_path)
series_df = get_df(series_file_path)