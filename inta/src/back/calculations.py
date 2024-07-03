import numpy as np
import math
import decimal
import matplotlib.pyplot as plt
from src import config

decimal.getcontext().prec = config.PRECISION

class Calculations:
    def __init__(self,gui_services , *args):
        self.gui_services = gui_services
        self.args = args
        
    def calculate_magnetic_moment(self, sensor_data: dict, distances: list) -> list:
        try:
            if sensor_data is None:
                raise ValueError("sensor_data is None")

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

                self._plot_calculation_graphs(inverted_distances, halved_substractions, axis)
                slope = self._slope_calculation(np.array(halved_substractions).astype(np.float64), np.array(inverted_distances).astype(np.float64))
                
                result = (slope / config.MOMENTUM) * config.FINAL_MOMENTUM
                results.append(result)
                
            return results
        except ValueError as e:
            self.gui_services.log_error("ValueError", str(e))
            raise e
        except Exception as e: 
            self.gui_services.log_error("Exception", str(e))
            raise e
    
    def _invert_cube_distance(self, distances_list: list) -> list:
        result_list = []
        for distance in distances_list:
            try:
                result = math.pow( 1 / float(distance), 3 )
                result_list.append(result)
            except ZeroDivisionError as e:
                self.gui_services.log_error("Distance value cannot be 0", str(e))
                
        return result_list
    
    
    def _substraction_halving(self, minuend :float, subtrahend :float) -> float:
        return (minuend - subtrahend) / 2
    
    
    def _slope_calculation(self, y_axis: np.ndarray, x_axis: np.ndarray) -> float:
        slope, intercept = np.polyfit(x_axis, y_axis, 1)
        
        return slope
    
    
    def _plot_calculation_graphs(self, x_axis: list, series: list, name_axis: str) -> str:
        fig, ax = plt.subplots()
        ax.plot(x_axis, series)
        ax.set_title(f'{name_axis} Axis Plot')
        ax.set_xlabel('Inverted Distance Cubed')
        ax.set_ylabel('Halved Substraction Average')
        plot_name = f'{name_axis}_axis_graph.png'
        fig.savefig(f'src/front/resource/{plot_name}')
        plt.close(fig)
        
        return f'src/front/resource/{plot_name}'
    

    def _rounded_number(self, num: float) -> float:
        return round(num, 15)

    # def _example_of_usign_decimal(self):
    #     var1 = decimal.Decimal(str(1.4444))
    #     var2 = decimal.Decimal(str(2.2333))
    #     pass
