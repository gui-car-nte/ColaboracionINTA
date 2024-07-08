# Technical Documentation: Magnetic Moment Calculation Algorithm
## Overview
    This document provides a comprehensive description of the algorithm developed to calculate the magnetic moment from sensor data. The algorithm processes sensor readings, computes relevant intermediate values, and ultimately determines the magnetic moment along three axes (X, Y, and Z).

## Table of Contents
1. Introduction
2. Input Data
3. Algorithm Steps
    1. Invert Cube Distance
    2. Halved Subtraction Calculation
    3. Slope Calculation
    4. Magnetic Moment Calculation
4. Plotting and Visualization
5. Error Handling
6. Output

## 1. Introduction
The magnetic moment calculation algorithm is designed to analyze sensor data from multiple sensors positioned at known distances from a magnetic source. The algorithm computes the magnetic moment by following a series of mathematical operations and transformations on the sensor data.

## 2. Input Data
The algorithm requires the following inputs:

Sensor Data: A dictionary containing DataFrames for sensor readings along the X, Y, and Z axes. Each DataFrame contains readings from multiple sensors.

Distances: A list of distances from each sensor to the magnetic source.
## 3. Algorithm Steps
**The algorithm performs the following steps to compute the magnetic moment:**

### A. Invert Cube Distance
`Function: _invert_cube_distance(distances_list: list) -> list`

This function computes the inverse of the cube of each distance in the input list. The mathematical operation for each distance 𝑑 is:

### inverted_distance =  ($1 \over 𝑑$)$^3$

Step-by-Step:

- Iterate over each distance in the input list.
- Compute the inverted cube distance for each distance.
- Append the result to the result list.
- Return the result list.
- Example:

        Input: [2, 4, 6]
        Output: [0.125, 0.015625, 0.00462963]

### B. Halved Subtraction Calculation
`Function: _substraction_halving(minuend: float, subtrahend: float) -> float`

This function computes the halved difference between two values. The mathematical operation is:

### halved_subtraction = ($minuend−subtrahend \over 2 $)


## C. Slope Calculation

`Function: _slope_calculation(y_axis: np.ndarray, x_axis: np.ndarray) -> float`

This function computes the slope of the linear regression line fitted to the data points defined by the x and y axes. The slope is determined using the least squares method.

    Step-by-Step:

    - Convert the input lists to NumPy arrays.
    - Use the np.polyfit function to fit a linear regression line to the data points.
    - Extract the slope from the result.
    - Return the slope.

## D. Magnetic Moment Calculation
`Main Function: calculate_magnetic_moment(sensor_data: dict, distances: list) -> list`

**This function integrates the previous steps to compute the magnetic moment along each axis.**

    Step-by-Step:
    - Validate the input data.
    - Clear any previous calculation steps.
    - Compute the inverted cube distances.

    For each axis (X, Y, Z):
    - Initialize a list to store halved subtractions.
    - Plot the calculation graph.
        
    For each sensor:
    - Extract the plus and minus average values from the sensor data.
    - Compute the halved subtraction.
    - Append the halved subtraction to the list.
    - Compute the slope of the halved subtractions versus inverted distances.
    - Calculate the magnetic moment using the formula:
magnetic_moment = ($ slope \over config.MOMENTUM $) $× config.FINALMOMENTUM$

    - Append the magnetic moment to the results list.
    - Return the results list.

## 4. Plotting and Visualization
`Function: _plot_calculation_graphs(x_axis: list, series: list, name_axis: str) -> str`

This function generates a plot for the halved subtractions against the inverted cube distances and saves the plot as an image file.

Step-by-Step:

Create a plot using Matplotlib.
Plot the series data against the x-axis data.
Set the title, xlabel, and ylabel for the plot.
Save the plot as an image file.
Close the plot to free resources.
Return the file path of the saved plot.

## 5. Error Handling
The algorithm includes error handling to ensure robustness. Errors are logged and reported through the gui_services interface. Common errors handled include:

Value errors when sensor data is None.
ZeroDivisionError when distances contain zero values.

## 6. Output
The main output of the algorithm is a list of magnetic moments for the X, Y, and Z axes. Additionally, the detailed calculation steps are logged and can be retrieved for debugging or review purposes.

Example:

    Magnetic Moments: [moment_X, moment_Y, moment_Z]
    Calculation Steps: A detailed log of each step performed during the calculation.
