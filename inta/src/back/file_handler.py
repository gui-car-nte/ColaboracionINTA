import pandas as pd
import os

class FileHandler:
    def __init__(self, filepaths=None):
        self.data = {}
        if filepaths:
            self.load_csv_files(filepaths)

    def load_csv_files(self, filepaths):
            try:
                csv_data_dict = {}
                for path in filepaths:
                    df = pd.read_csv(path)
                    filename = self._extract_filename(path)
                    csv_data_dict[filename] = df
                    
                return csv_data_dict
            except FileNotFoundError:
                print(f"File not found: {path}")
            except pd.errors.ParserError:
                print(f"Parse error at: {path}")
            except Exception as e:
                raise e
    
    # TODO  
    def count_sensors(self):
        pass

    def _extract_filename(self, filepath):
        return os.path.basename(filepath).split('.')[0]