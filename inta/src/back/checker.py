import pandas as pd

class Checker:
    def __init__(self, gui_services):
        self.gui_services = gui_services
    
    def check_csv_format(self, filepath: str):
        try:
            df = pd.read_csv(filepath)
            if df.shape[0] < 2:
                raise ValueError(f"File does not have enough rows for data validation: {filepath}")

            second_row = df.iloc[1]
            if not all(second_row.apply(lambda x: self.is_numeric(x))):
                raise ValueError(f"Non-numeric data found in the second row of file: {filepath}")
        except ValueError as e:
            self.gui_services.log_error("File Format Error", str(e))
            raise

    def is_numeric(self, value):
        try:
            float(value)
            return True
        except ValueError as e:
            return False

    def check_consistent_sensor_count(self, data: dict):
        try:
            keys = data.keys()
            sensors = []
            for key in keys:
                sensors.append(data[key].shape[1] / 3)

            prv = 0
            for sensor in sensors:
                if prv == 0:
                    prv = sensor
                if sensor != prv:
                    raise ValueError('Files have different numbers of sensors')
        except ValueError as e:
            self.gui_services.log_error("File Format Error", str(e))
            raise
