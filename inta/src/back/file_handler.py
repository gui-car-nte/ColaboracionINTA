import pandas as pd
import os
# from inta.src.config import CSV_NAMES
from src.front.settings import CSV_NAMES
from src.back.checker import Checker

class FileHandler:
    def __init__(self, filepaths: list, gui_services):
        self.data = {}
        self.checker = Checker(gui_services)
        if filepaths:
            self.load_csv_files(filepaths)

    def load_csv_files(self, filepaths: list):
        if len(filepaths) != 6:
            self.checker.gui_services.log_error("File Count Error", f"Expected 6 files, but got {len(filepaths)}")
            raise ValueError(f"Expected 6 files, but got {len(filepaths)}")

        filenames = [self._extract_filename(path) for path in filepaths]
        if set(filenames) != set(CSV_NAMES):
            self.checker.gui_services.log_error("Filename Error", f"Filenames do not match the expected names: {CSV_NAMES}")
            raise ValueError(f"Filenames do not match the expected names: {CSV_NAMES}")

        try:
            for path in filepaths:
                self.checker.check_csv_format(path)

                df = pd.read_csv(path)
                filename = self._extract_filename(path)
                self.data[filename] = df

            self.checker.check_consistent_sensor_count(self.data)
            return self.data

        except FileNotFoundError as e:
            self.checker.gui_services.log_error("File Not Found", f"File not found: {path}")
            raise FileNotFoundError(f"File not found: {path}") from e
        except pd.errors.ParserError as e:
            self.checker.gui_services.log_error("Parse Error", f"Parse error at: {path}")
            raise ValueError(f"Parse error at: {path}") from e
        except Exception as e:
            self.checker.gui_services.log_error("Exception", str(e))
            raise
            
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
                self.checker.gui_services.log_error("Sensor Count Error", 'Files have different numbers of sensors')
                raise ValueError('Files have different numbers of sensors')

        return int(prv)

    def _extract_filename(self, filepath: str) -> str:
        return os.path.basename(filepath).split('.')[0]
