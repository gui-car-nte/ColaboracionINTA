import pandas as pd
import os


# TODO data typing in methods
class FileHandler:
    def __init__(self, filepaths):
        self.data = {}
        if filepaths:
            self.load_csv_files(filepaths)


    def load_csv_files(self, filepaths: list):
            try:
                for path in filepaths:
                    df = pd.read_csv(path)
                    filename = self._extract_filename(path)
                    self.data[filename] = df
    
                return self.data
            except FileNotFoundError:
                print(f"File not found: {path}")
            except pd.errors.ParserError:
                print(f"Parse error at: {path}")
            except Exception as e:
                raise e
    
    
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
                print('Diferentes cantidades de sensores')

        return int(prv)
    
    
    def _extract_filename(self, filepath: str) -> str:
        return os.path.basename(filepath).split('.')[0]