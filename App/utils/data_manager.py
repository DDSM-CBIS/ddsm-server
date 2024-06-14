import pandas as pd
import re

class DataManager:
    def __init__(self):
        self.calc_df: pd.DataFrame = None
        self.mass_df: pd.DataFrame = None
        self.df: pd.DataFrame = None
        self.config = None

    def set_config(self, config):
        self.config = config

    @staticmethod
    def get_df(file_path):
        file = pd.read_csv(file_path)
        renamed_columns = {col: col.replace(" ", "_") for col in file.columns}
        return file.rename(columns=renamed_columns)

    @staticmethod
    def convert_key_format(key, keys_format = "camel"):
        """
        Convert key to the specified format.

        Parameters
        ----------
        key: str
            The key to convert
        keys_format: str
            The format to convert the key to. Options are "camel", "snake", "camel_space", "upper-snake"

        Returns
        -------
        str
            The converted key
        """
        if keys_format == 'camel':
            return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), key)
        elif keys_format == 'snake':
            return key
        elif keys_format == 'camel_space':
            return re.sub(r'_([a-z])', lambda x: ' ' + x.group(1).upper(), key)
        elif keys_format == 'upper-snake':
            return key.upper()
        else:
            raise ValueError("Invalid keys_format. Options are 'camel', 'snake', 'camel_space', 'upper-snake'")

    def set_calc_df(self):
        self.calc_df = self.get_df(self.config["calc_file_path"])

    def set_mass_df(self):
        self.mass_df = self.get_df(self.config["mass_file_path"])
    
    def set_df(self):
        self.df = pd.merge(self.calc_df, self.mass_df, how="outer")

    def get_columns(self, collection : str, include_file_path : bool = False):
        calc_columns = set(self.calc_df.columns)
        mass_columns = set(self.mass_df.columns)

        if collection == "common":
            columns = calc_columns.intersection(mass_columns)
        elif collection == "distinct":
            columns = calc_columns.symmetric_difference(mass_columns)

        if not include_file_path:
            columns = [col for col in columns if "file_path" not in col]

        return columns
    
    def get_unique_values(self, collection: str, keys_format = "camel", include_file_path : bool = False):
        columns = self.get_columns(collection, include_file_path)
        unique_values = {col: set() for col in columns}

        for col in columns:
            if col in self.df.columns:
                unique_values[col].update(self.df[col].dropna().unique())
            
        unique_values = {self.convert_key_format(k, keys_format): list(v) for k, v in unique_values.items()}
        return unique_values

    def get_patient_ids(self):
        return self.df["patient_id"].unique()
        
    def get_patients_data(self, keys_format: str = "camel", include_file_path : bool = False, patient_id = None):
        """
        Get data for all patients

        Parameters
        ----------
        keys_format: str
            The format of the keys in the data. Options are "camel", "snake", "camel_space", "upper-snake"
        include_file_path: bool
            Whether to include the file path columns in the data
        patient_id: str
            The patient id to get data for. If None, data for all patients is returned
        
        Returns
        -------
        dict
            The data for all patients
        """

        patients_data = self.df

        if patient_id:
            patients_data = patients_data[patients_data["patient_id"] == patient_id]

        if not include_file_path:
            patients_data = patients_data[[col for col in patients_data.columns if "file_path" not in col]]
        
        patients_data = patients_data.dropna(axis=1, how="any")
        patients_data = patients_data.rename(columns={col: self.convert_key_format(col, keys_format) for col in self.df.columns})

        patients_dict = {}
        grouped = patients_data.groupby(self.convert_key_format('patient_id', keys_format))

        for p_id, group in grouped:
            patient_list = [
                {k: v for k, v in row.items() if pd.notnull(v) and k != self.convert_key_format('patient_id', keys_format)}
                for row in group.to_dict(orient='records')
            ]
            patients_dict[p_id] = patient_list

        return patients_dict

    def start(self, config):
        self.set_config(config)
        self.set_calc_df()
        self.set_mass_df()
        self.set_df()