import math
import numpy as np
import pandas as pd
import os
import decimal

MOMENTUM = 0.0000002
FINAL_MOMENTUM = 1000
decimal.getcontext().prec = 15

def calculate_magnetic_moment(sensor_data, distances: list) -> list:
    results = []
    inverted_distances = _invert_cube_distance(distances)

    for axis in ['X', 'Y', 'Z']:
        print(f'current big axis: {axis}')
        semi_subtractions = []
        for sensor in range(len(distances)):
            print(f'\n>>>>> getting data for sensor {sensor + 1}')
            sensor_number = (sensor * 3)
            avg_add = sensor_data[f'{axis}mas'].iloc[:, sensor_number].mean()
            avg_sub = sensor_data[f'{axis}menos'].iloc[:, sensor_number].mean()
            semi_sub = _semi_substraction(avg_add, avg_sub)
            print(f'current file: {axis}mas, scanning column {sensor_number}, average: {avg_add}\ncurrent file: {axis}menos, scanning column {sensor_number}, average: {avg_sub}\nsemi substraction: {semi_sub}')
            semi_subtractions.append(semi_sub)
            
        print(f'\nabout to do slope calc\nsemi subs list: {semi_subtractions}\ninverted distances list: {inverted_distances}')
        slope = _slope_calculation(semi_subtractions, inverted_distances)
        print(f'slope calculation: {slope}')
        
        result = (slope / MOMENTUM) * FINAL_MOMENTUM
        print(f'axis {axis} calculation: {result}')
        results.append(result)
        
    return results

def _invert_cube_distance(nums: list) -> list:
    ope_list = []
    for num in nums:
        operated = math.pow( 1 / (num), 3 )
        ope_list.append(operated)
    return ope_list

def _semi_substraction(num1, num2):
    ope = (num1 - num2) / 2
    return ope

def _slope_calculation(y_axis: list, x_axis: list) -> float:
    y_axis = np.array(y_axis)
    x_axis = np.array(x_axis)

    slope, intercept = np.polyfit(x_axis, y_axis, 1)

    return slope

def extract_filename(filepath):
    return os.path.basename(filepath).split('.')[0]

filepaths = ['/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Xmas.csv', '/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Xmenos.csv', '/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Ymas.csv', '/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Ymenos.csv', '/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Zmas.csv', '/home/guillermo-carrillo/github/ColaboracionINTA/docs/calculos/Zmenos.csv']

def load_csv_files(filepaths):
            try:
                csv_data_dict = {}
                for path in filepaths:
                    df = pd.read_csv(path)
                    filename = extract_filename(path)
                    csv_data_dict[filename] = df
                    
                return csv_data_dict
            except FileNotFoundError:
                print(f"File not found: {path}")
            except pd.errors.ParserError:
                print(f"Parse error at: {path}")
            except Exception as e:
                raise e
            
sensors_data = load_csv_files(filepaths)
distances = [0.5, 0.532, 0.576, 0.608, 0.669, 0.773, 1]

results = calculate_magnetic_moment(sensors_data, distances)
print(f'the final result is: {results}')