import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import os

source_folder = f"D:/7.27.22/ondrive/LAB/StemConduction/newraw/"

i = 1   # this is just for logging during development

for file in os.listdir(source_folder):

    df = pd.read_csv(os.path.join(source_folder, file), header=1, skiprows=[2, 3])

    def fix_timestamps(stamp):
        if '.' in stamp:
            return stamp
        else:
            stamp += '.00'
            return stamp

    raw_timestamps = df["TIMESTAMP"]
    timestamps = pd.to_datetime(raw_timestamps.apply(fix_timestamps))    
    records = df["RECORD"]
    temperatures = df["Temp_C_1"]

    if file == "pintae0701a.csv":          # this file has a two-second run of NAN readings
        rows_to_drop = list(range(1025, 1044))
        temperatures = temperatures.drop(rows_to_drop)
        records = records.drop(rows_to_drop)
        timestamps = timestamps.drop(rows_to_drop)

    x_data = records.iloc[361:]

    y_data = temperatures.iloc[361:]

    def poly_func(x, a, b, c):
        return a * x**2 + b * x + c

    params, params_covariance = curve_fit(poly_func, x_data, y_data)

    # print(params)

    x_fit = np.linspace(0, max(x_data), 100)
    y_fit = poly_func(x_fit, params[0], params[1], params[2])

    A = params[0]
    B = params[1]
    C = params[2] - 20

    x_of_20 = (-B + np.sqrt(B**2 - 4 * A * C)) / (2 * A)
    print(i, x_of_20)

    i += 1

    # plt.plot(x_data, y_data, label="Data", color='red')
    # plt.plot(x_fit, y_fit, label='fitted polynomial curve')
    # plt.scatter(x_of_20, 20)
    # plt.xlabel('sample')
    # plt.ylabel('temperature')
    # plt.legend()
    # plt.show()

