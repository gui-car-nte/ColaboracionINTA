import pandas as pd

class FileHandler:
    def __init__(self, filepaths=None):
        self.data = {}
        if filepaths:
            self.load_csv_files(filepaths)

    def load_csv_files(self, filepaths):
            try:
                # csv_data_dict = {}
                for path in filepaths:
                    print(path)
                    df = pd.read_csv(path)
                    # csv_data_dict[path] = df
                    self.data[path] = df
                    
                # return csv_data_dict
                return self.data
            except FileNotFoundError:
                print(f"File not found: {path}")
            except pd.errors.ParserError:
                print(f"Parse error at: {path}")
            except Exception as e:
                raise e
    
    def count_sensors(self):
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

