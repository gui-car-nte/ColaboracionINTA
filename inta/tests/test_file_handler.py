import unittest
import pandas as pd
import os
from unittest.mock import MagicMock, patch
from src.config import CSV_NAMES
from src.back.checker import Checker
from src.back.file_handler import FileHandler  # Asumiendo que la clase FileHandler está en un archivo llamado file_handler.py

class TestFileHandler(unittest.TestCase):
    
    @patch('src.back.checker.Checker')
    def setUp(self, MockChecker):
        self.mock_checker = MockChecker()
        self.mock_checker.gui_services = MagicMock()
        self.filepaths = [f"{name}.csv" for name in CSV_NAMES]
        
        # Mocking the content of the CSV files
        self.mock_data = {name: pd.DataFrame({
            'sensor_1_x': [0, 1, 2],
            'sensor_1_y': [0, 1, 2],
            'sensor_1_z': [0, 1, 2],
            'sensor_2_x': [3, 4, 5],
            'sensor_2_y': [3, 4, 5],
            'sensor_2_z': [3, 4, 5],
        }) for name in CSV_NAMES}

        for path, df in zip(self.filepaths, self.mock_data.values()):
            df.to_csv(path, index = False)

        self.file_handler = FileHandler(self.filepaths, self.mock_checker.gui_services)

    def tearDown(self):
        for path in self.filepaths:
            if os.path.exists(path):
                os.remove(path)

    def test_load_csv_files_success(self):
        data = self.file_handler.load_csv_files(self.filepaths)
        self.assertEqual(len(data), 6)
        for name in CSV_NAMES:
            self.assertTrue(name in data)
            pd.testing.assert_frame_equal(data[name], self.mock_data[name])

    def test_load_csv_files_file_count_error(self):
        with self.assertRaises(ValueError):
            self.file_handler.load_csv_files(self.filepaths[:-1])

    def test_load_csv_files_filename_error(self):
        invalid_filepaths = self.filepaths[:-1] + ['invalid.csv']
        with self.assertRaises(ValueError):
            self.file_handler.load_csv_files(invalid_filepaths)

    def test_load_csv_files_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.file_handler.load_csv_files(['non_existent.csv'] * 6)

    def test_load_csv_files_parse_error(self):
        with open(self.filepaths[0], 'w') as f:
            f.write("invalid content")
        
        with self.assertRaises(ValueError):
            self.file_handler.load_csv_files(self.filepaths)

    def test_count_sensors_success(self):
        self.file_handler.data = self.mock_data
        count = self.file_handler.count_sensors()
        self.assertEqual(count, 2)

    def test_count_sensors_inconsistent_sensor_count(self):
        self.mock_data[CSV_NAMES[0]] = pd.DataFrame({
            'sensor_1_x': [0, 1, 2],
            'sensor_1_y': [0, 1, 2],
            'sensor_1_z': [0, 1, 2],
        })
        self.file_handler.data = self.mock_data
        with self.assertRaises(ValueError):
            self.file_handler.count_sensors()

if __name__ == '__main__':
    unittest.main()
