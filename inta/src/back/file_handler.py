import pandas as pd
import os
from src.config import CSV_NAMES
# from src.front.tkinter_settings import log_error


class FileHandler:
    def __init__(self, filepaths: list):
        self.data = {}
        if filepaths:
            self.load_csv_files(filepaths)


    def load_csv_files(self, filepaths: list):
        if len(filepaths) != 6:
            raise ValueError(f"Expected 6 files, but got {len(filepaths)}")

        filenames = [self._extract_filename(path) for path in filepaths]
        if set(filenames) != set(CSV_NAMES):
            raise ValueError(f"Filenames do not match the expected names: {CSV_NAMES}")

        try:
            for path in filepaths:
                self._check_csv_format(path)

                df = pd.read_csv(path)
                filename = self._extract_filename(path)
                self.data[filename] = df

            self._check_consistent_sensor_count()

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except pd.errors.ParserError:
            raise ValueError(f"Parse error at: {path}")
        except Exception as e:
            raise e


    def _check_csv_format(self, filepath: str):
        with open(filepath, 'r') as file:
            first_line = file.readline()
            if not first_line:
                raise ValueError(f"File is empty: {filepath}")
            if ',' not in first_line:
                raise ValueError(f"Invalid CSV format in file: {filepath}")

        df = pd.read_csv(filepath, nrows=2)
        if df.shape[0] < 2:
            raise ValueError(f"File does not have enough rows for data validation: {filepath}")

        second_row = df.iloc[1]
        if not all(second_row.apply(lambda x: pd.api.types.is_numeric_dtype(x))):
            raise ValueError(f"Non-numeric data found in the second row of file: {filepath}")


    def _check_consistent_sensor_count(self):
        keys = self.data.keys()
        sensors = []
        for key in keys:
            sensors.append(self.data[key].shape[1] / 3)

        prv = 0
        for sensor in sensors:
            if prv == 0:
                prv = sensor
            if sensor != prv:
                raise ValueError('Files have different numbers of sensors')
            
            
    def count_sensors(self) -> int:
        keys = self.data.keys()
        sensors = []
        for key in keys:
            sensors.append(self.data[key].shape[1] / 3)

        prv = 0
        for sensor in sensors:
            if prv == 0:
                prv = sensor
            if sensor != prv:
                raise ValueError('Files have different numbers of sensors')

        return int(prv)
    
    
    def _extract_filename(self, filepath: str) -> str:
        return os.path.basename(filepath).split('.')[0]