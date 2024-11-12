import pandas as pd
import numpy as np
from lacbox.io import load_oper
import matplotlib.pyplot as plt
wind_speeds = np.arange(5, 25, 1)


bins = [(ws - 0.5, ws + 0.5) for ws in wind_speeds]
print("Bins:", bins)

# Calculate probabilities for each wind speed
probabilities = []
for ws in wind_speeds:
    a = ((ws - 0.5)**2 * np.pi) / 225
    b = ((ws + 0.5)**2 * np.pi) / 225
    prob = np.exp(-a) - np.exp(-b)
    probabilities.append(prob)


filename1 = 'our_design/data/Group1_redesign_flex.opt'
opt_data1 = load_oper(filename1)
print(opt_data1.keys())
# Display the data to confirm it's loaded correctly
wind_speeds_redesign = opt_data1['ws_ms']
aero_power_redesign = opt_data1['power_kw']
for ws, power in zip(wind_speeds_redesign, aero_power_redesign):
    print(f"Wind Speed: {ws} m/s, Aero Power: {power} kW")
probabilities_normal = [float(f"{p:.4f}") for p in probabilities]
print("Probabilities:", probabilities_normal)
# print("Size of probabilities:", probabilities_normal.size)

filtered_wind = []
filtered_power = []

for w, p in zip(wind_speeds_redesign, aero_power_redesign):
    if w.is_integer():
        filtered_wind.append(w)
        filtered_power.append(p)


# Result

filtered_wind = filtered_wind[1:-1]  # Exclude the first and last elements
filtered_power = filtered_power[1:-1]
filtered_power = np.array(filtered_power)
probabilities_normal = np.array(probabilities_normal)
Power_total= probabilities_normal*filtered_power
total_sum = np.sum(Power_total)*8760
aep_gwh_3B= total_sum/1e6
print(f"AEP of 3B redesigned Turbine: {aep_gwh_3B:.2f} GWh")


filename2= 'dtu_10mw/data/dtu_10mw_flex_minrotspd.opt'
opt_data2= load_oper(filename2)
print(opt_data2.keys())
wind_speeds_DTU= opt_data2['ws_ms']
aero_power_DTU= opt_data2['power_kw']

filtered_wind_DTU = []
filtered_power_DTU = []

for w1, p1 in zip(wind_speeds_DTU, aero_power_DTU):
    if w1.is_integer():
        filtered_wind_DTU.append(w1)
        filtered_power_DTU.append(p1)
filtered_wind_DTU = filtered_wind_DTU[1:-1]  # Exclude the first and last elements
filtered_power_DTU = filtered_power_DTU[1:-1]
filtered_power_DTU = np.array(filtered_power_DTU)

Power_total_DTU= probabilities_normal*filtered_power_DTU
total_sum_DTU = np.sum(Power_total_DTU)*8760
aep_gwh_3A= total_sum_DTU/1e6
print(f"AEP of DTU 3A Turbine: {aep_gwh_3A:.2f} GWh")


plt.plot(filtered_wind_DTU, filtered_power_DTU, label='Filtered Power DTU')

# Plot the second line (aero_power_redesign vs filtered_wind_DTU)
plt.plot(filtered_wind_DTU, filtered_power, label='Aero Power Redesign')
plt.title("Power Curve")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Weighted Power")
plt.legend()
 # Save the plot as a PNG image
plt.show()

plt.plot(filtered_wind_DTU, probabilities_normal)
plt.title("Probabilities")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Probability")
plt.legend()
plt.show()