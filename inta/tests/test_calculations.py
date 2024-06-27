import math
import numpy as np

MOMENTUM = 0.0000002
FINAL_MOMENTUM = 1000

def calculate_magnetic_moment(sensor_data: dict, distances: list) -> list:
    results = []
    inverted_distances = _invert_cube_distance(distances)

    for axis in ['X', 'Y', 'Z']:
        semi_subtractions = []
        for sensor in range(len(distances)):
            avg_add = sensor_data[f'{axis}mas'].iloc[:, sensor*3].mean()
            avg_sub = sensor_data[f'{axis}menos'].iloc[:, sensor*3].mean()
            semi_sub = _semi_substraction(avg_add, avg_sub)
            semi_subtractions.append(semi_sub)

        slope = _slope_calculation(semi_subtractions, inverted_distances)
        
        result = (slope / MOMENTUM) * FINAL_MOMENTUM
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
