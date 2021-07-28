#!/usr/bin/python3.8

# Importing necessary libraries
import numpy as np
import pandas as pd

# Reading the data from the stored csv file
data = pd.read_csv('q2_temp_data.csv')

# Raising an alert if the temperature at any point crosses 200K
c = 0
for _, reading in data.iterrows():
    if reading['Temperature (K)'] >= 200.0:
        print(f"FAILURE @ {reading['Total Time (mins)']:4.0f} mins! : Temperature of {reading['Temperature (K)']:7.4f}K (>200K) is measured by the thermocouple")
        c += 1

if c > 0:
    print("As per protocol, this vaccine container is unfit for use.")
