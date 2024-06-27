import numpy as np
import math
import decimal
from src.config import *

decimal.getcontext().prec = PRECISION

class Calculations:
    
    def __init__(self, *args):
        self.args = args
    
    def calculate_magnetic_moment(self, sensor_data: dict, distances: list) -> list:
        results = []
        inverted_distances = self._invert_cube_distance(distances)

        for axis in ['X', 'Y', 'Z']:
            halved_substractions = []
            for sensor in range(len(distances)):
                sensor_number = (sensor * 3)
                plus_average = sensor_data[f'{axis}mas'].iloc[:, sensor_number].mean()
                minus_average = sensor_data[f'{axis}menos'].iloc[:, sensor_number].mean()
                halved_substraction = self._substraction_halving(plus_average, minus_average)
                halved_substractions.append(halved_substraction)

            slope = self._slope_calculation(halved_substractions, inverted_distances)
            
            result = (slope / MOMENTUM) * FINAL_MOMENTUM
            results.append(result)
            
        return results
    
    def _invert_cube_distance(self, distances_list: list) -> list:
        result_list = []
        for distance in distances_list:
            result = math.pow( 1 / float(distance), 3 )
            result_list.append(result)
            
        return result_list
    
    def _substraction_halving(self, minuend, subtrahend):
        result = (minuend - subtrahend) / 2
        
        return result
    
    def _slope_calculation(self, y_axis: list, x_axis: list) -> float:
        y_axis = np.array(y_axis)
        x_axis = np.array(x_axis)
        slope, intercept = np.polyfit(x_axis, y_axis, 1)
        
        return slope
    
    def _rounded_number(self, num):
        return round(num, 15)

    
    # def _example_of_usign_decimal(self):
    #     var1 = decimal.Decimal(str(1.4444))
    #     var2 = decimal.Decimal(str(2.2333))
    #     pass
