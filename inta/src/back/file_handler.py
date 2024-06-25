import pandas as pd


class FileHandler:
    
    def __init__(self):
        self.data = []

    def load_csv_files(self, filepaths):
        for path in filepaths:
            print(f'ruta: {path}')
            df = pd.read_csv(path)
            self.data.append(df)
        return self.data
    
    def count_sensors():
        pass