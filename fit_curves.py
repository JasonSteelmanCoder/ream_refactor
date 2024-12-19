import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import os

## set input and output locations
source_folder = f"D:/7.27.22/ondrive/LAB/StemConduction/newraw/"
output_file = f"C:/Users/{os.getenv("MS_USER_NAME")}/Desktop/Ream/durations.csv"

i = 1   # this is just for logging during development

## define functions to use later
def fix_timestamps(stamp):
    if '.' in stamp:
        return stamp
    else:
        stamp += '.00'
        return stamp
    
def poly_func(x, a, b, c):
    return a * x**2 + b * x + c

## set up empty data frame to be populated later
output = pd.DataFrame(columns=["file", "duration"])

## loop through the files in the source folder, adding to the output data frame on each instance of the loop
for file in os.listdir(source_folder):

    ## read the file
    df = pd.read_csv(os.path.join(source_folder, file), header=1, skiprows=[2, 3])

    ## grab data from the file
    raw_timestamps = df["TIMESTAMP"]
    timestamps = pd.to_datetime(raw_timestamps.apply(fix_timestamps), format='%Y-%m-%d %H:%M:%S.%f')    
    records = df["RECORD"]
    temperatures = df["Temp_C_1"]

    ## correct for one file with a run of NAN readings
    if file == "pintae0701a.csv":          # this particular file has a two-second run of NAN readings
        rows_to_drop = list(range(1025, 1044))
        temperatures = temperatures.drop(rows_to_drop)
        records = records.drop(rows_to_drop)
        timestamps = timestamps.drop(rows_to_drop)

    ## define data to use in modeling curves
    ## we skip the first 360 data entries, since they are less reliable than the rest of the data
    x_data = records.iloc[361:]
    y_data = temperatures.iloc[361:]

    ## find the row where the temperature hits 60 degrees
    row_60_degrees = y_data.loc[pd.to_numeric(y_data) >= 60].first_valid_index()

    ## fit a polynomial to the data
    params, params_covariance = curve_fit(poly_func, x_data, y_data)

    # print(params)

    x_fit = np.linspace(0, max(x_data), 100)
    y_fit = poly_func(x_fit, params[0], params[1], params[2])

    A = params[0]
    B = params[1]
    C = params[2] - 20

    ## calculate the x value where the regression curve crosses 20 degrees
    x_of_20 = (-B + np.sqrt(B**2 - 4 * A * C)) / (2 * A)
    
    ## each data entry is 0.12 seconds apart
    ## calculate duration by multiplying count of entries between 20 degrees and 60 degrees by 0.12
    duration = (row_60_degrees - x_of_20) * 0.12
    if file == "pintae0701a.csv":             # since this file has a two second run of NAN readings, the time has to be added back to the duration.
        duration += (19 * 0.12)
    # print(duration)

    ## add a new row to the output with the file name and the duration from 20 degrees to 60 degrees
    new_row = {"file": file, "duration": int(duration)}
    output.loc[len(output)] = new_row

    ## increment i for easy logging
    i += 1

    ## uncomment to see a visualization of the curve fit
    # plt.plot(x_data, y_data, label="Data", color='red')
    # plt.plot(x_fit, y_fit, label='fitted polynomial curve')
    # plt.scatter(x_of_20, 20)
    # plt.xlabel('sample')
    # plt.ylabel('temperature')
    # plt.legend()
    # plt.show()

## save the dataframe to a csv file
output.to_csv(output_file, index=False)