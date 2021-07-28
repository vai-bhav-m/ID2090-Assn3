#!/usr/bin/python3.8

# Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# for storing the time and temperatures at each instant
Time = []
Temperature = []

# base temperature value of 77 K (given in the question)
Temp_base = 77
Temp_rise_rate = np.random.rand()    # Linear rate of increase of temperature with unit K/min


# Sample case where I am refilling the vaccine containers 10 times
for i in range(10):
    Refill_time = np.random.randint(np.floor((200-77)/Temp_rise_rate - 20),np.floor(123/Temp_rise_rate + 5))       # refilling after random time intervals
    Temperature.append(Temp_base)
    Time.append(0)

    for t in range(1,Refill_time):
        Temperature.append(Temperature[-1] + Temp_rise_rate)
        Time.append(t)

# Storing this dummy data in a pandas DataFrame
data=pd.DataFrame({
    'Time (mins)': list(Time),
    'Temperature (K)':list(Temperature)
})

data['Total Time (mins)'] = np.arange(len(data))  # Adding a column corresponding to the total time of the experiment

# Plotting the accumulated data. Every vertical line signifies a change of state when the container is refilled and the
# experiment is started again at 77 K
plt.plot(data['Total Time (mins)'], data['Temperature (K)'])
plt.title('Temperature vs Total Time plot for vaccine container')
plt.xlabel('Total Time (mins)')
plt.ylabel('Temperature (K)')
plt.savefig('q2_temp_time_plot.png')

# From the graph we can easily conclude that there are some instances when the temperature rose beyond 200K

# Saving the dataframe in csv format for the data validation script to utilise
data.to_csv('q2_temp_data.csv', index=False )
