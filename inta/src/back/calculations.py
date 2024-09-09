import numpy as np
import math
import decimal
import matplotlib.pyplot as plt
from src.config import *

decimal.getcontext().prec = PRECISION

class Calculations:
    def __init__(self, gui_services, *args):
        self.gui_services = gui_services
        self.args = args
        self.steps = []
        
    def calculate_magnetic_moment(self, sensor_data: dict, distances: list) -> list:
        try:
            if sensor_data is None:
                raise ValueError("No sensor data provided")
            
            self.steps.clear()
            results = []
            inverted_distances = self._invert_cube_distance(distances)
            
            for axis in ['X', 'Y', 'Z']:
                halved_substractions = []
                
                for sensor in range(len(distances)):
                    sensor_number = (sensor * 3)
                    
                    try:
                        plus_col_name = f'{axis}mas' 
                        minus_col_name = f'{axis}menos'
                        
                        if plus_col_name not in sensor_data or minus_col_name not in sensor_data:
                            self.steps.append(f'Skipping sensor {sensor + 1} for {axis} axis: Data not available')
                            continue
                        
                        plus_average = sensor_data[plus_col_name].iloc[START_ROW:END_ROW, sensor_number].mean()
                        minus_average = sensor_data[minus_col_name].iloc[START_ROW:END_ROW, sensor_number].mean()
                        
                        halved_substraction = self._substraction_halving(plus_average, minus_average)
                        halved_substractions.append(halved_substraction)
                        self.steps.append(f'{axis} axis sensor {sensor + 1}: halved substraction = {halved_substraction:.15f}')
                    
                    except KeyError as e:
                        self.steps.append(f'Sensor {sensor + 1} for {axis} axis missing data: {str(e)}')
                        self.gui_services.log_error("Missing Data", str(e))
                        continue
                
                if len(halved_substractions) > 0:
                    self._plot_calculation_graphs(inverted_distances, halved_substractions, axis)
                    slope = self._slope_calculation(np.array(halved_substractions).astype(np.float64), np.array(inverted_distances).astype(np.float64))
                    
                    momentum_decimal = decimal.Decimal(str(MOMENTUM))
                    final_momentum_decimal = decimal.Decimal(str(FINAL_MOMENTUM))

                    result = (slope / momentum_decimal) * final_momentum_decimal
                    self.steps.append(f'{axis} axis slope = {slope:.15f}')
                    results.append(result)
                
            return results
        
        except ValueError as e:
            self.gui_services.log_error("ValueError", str(e))
            self.steps.append(f'Error: {str(e)}')
            raise e
        except Exception as e: 
            self.gui_services.log_error("Exception", str(e))
            self.steps.append(f'Error: {str(e)}')
            raise e
    
    def _invert_cube_distance(self, distances_list: list) -> list:
        result_list = []
        for distance in distances_list:
            try:
                result = math.pow( 1 / float(distance), 3 )
                result_list.append(result)
                self.steps.append(f'Inverted distance^3 for {distance} = {result:.15f}')
            except ZeroDivisionError as e:
                self.gui_services.log_error("Distance value cannot be 0", str(e))
                self.steps.append(f'Error: {str(e)}')
                
        return result_list
    
    
    def _substraction_halving(self, minuend :float, subtrahend :float) -> decimal.Decimal:
        minuend_decimal = decimal.Decimal(str(minuend))
        subtrahend_decimal = decimal.Decimal(str(subtrahend))
        result = (minuend_decimal - subtrahend_decimal) / 2
        self.steps.append(f'Halved substraction: ({minuend} - {subtrahend}) / 2 = {result}')
        return result
    
    
    def _slope_calculation(self, y_axis: np.ndarray, x_axis: np.ndarray) -> decimal.Decimal:
        x_axis_decimal = [decimal.Decimal(str(x)) for x in x_axis]
        y_axis_decimal = [decimal.Decimal(str(y)) for y in y_axis]

        slope, intercept = np.polyfit(np.array(x_axis_decimal, dtype=np.float64), np.array(y_axis_decimal, dtype=np.float64), 1)
        slope_decimal = decimal.Decimal(str(slope))
        return slope_decimal
    
    
    def _plot_calculation_graphs(self, x_axis: list, series: list, axis_name: str) -> str:
        fig, ax = plt.subplots()
        ax.plot(x_axis, series)
        ax.set_title(f'{axis_name} Axis Plot')
        ax.set_xlabel('d^(-3)(m^-3)')
        ax.set_ylabel('B(T)')
        ax.grid()
        plot_name = f'{axis_name}_axis_graph.png'
        fig.savefig(f'src/front/resource/{plot_name}')
        plt.close(fig)
        
        return f'src/front/resource/{plot_name}'
    

    def _rounded_number(self, num: float) -> float:
        return round(num, 15)
    
    def get_calculation_steps(self) -> str:
        return '\n\n'.join(self.steps)
