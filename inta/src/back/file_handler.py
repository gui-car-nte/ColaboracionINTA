import pandas as pd

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
                    csv_data_dict[path] = df
                    
                return csv_data_dict
            except FileNotFoundError:
                print(f"File not found: {path}")
            except pd.errors.ParserError:
                print(f"Parse error at: {path}")
            except Exception as e:
                raise e
    
    def count_sensors(self):
        pass

