import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV files
df1 = pd.read_csv('Hourly_electricity_demand_net_generation_and_net_imports_for_New_England.csv')
df3 = pd.read_csv('Hourly_net_generation_by_energy_source_in_New_England.csv')

demand_actual = df1['demand megawatthours (MWh)'].values

#net generation by energy source
wind_energy = df3['wind megawatthours (MWh)'].values
solar_energy = df3['solar megawatthours (MWh)'].values
hydro_energy = df3['hydro megawatthours (MWh)'].values
natural_gas_energy = df3['natural gas megawatthours (MWh)'].values
coal_energy = df3['coal megawatthours (MWh)'].values
nuclear_energy = df3['nuclear megawatthours (MWh)'].values

#peak energy for each source
peak_wind = np.max(wind_energy)
peak_solar = np.max(solar_energy)
peak_hydro = np.max(hydro_energy)
peak_natural_gas = np.max(natural_gas_energy)
peak_coal = np.max(coal_energy)
peak_nuclear = np.max(nuclear_energy)

#arrays for optimized energy mix
optimized_renewable = np.zeros_like(demand_actual)
optimized_conventional = np.zeros_like(demand_actual)

#meet demand_actual
for i in range(len(demand_actual)):
    # Allocate renewable energy first
    renewable_energy = wind_energy[i] + solar_energy[i] + hydro_energy[i]
    if renewable_energy >= demand_actual[i]:
        optimized_renewable[i] += demand_actual[i]
    else:
        optimized_renewable[i] += renewable_energy
    
    # Allocate remaining demand to conventional sources, if necessary
    optimized_conventional[i] = demand_actual[i] - optimized_renewable[i]

# Plotting demand_actual and optimized energy mix
plt.figure(figsize=(12, 6))

plt.stackplot(df1.index, 
              optimized_renewable, optimized_conventional,
              labels=['Renewable Energy', 'Conventional Energy'],
              colors=['g', 'r'])

plt.plot(df1.index, demand_actual, label='Demand Actual', color='b')

plt.xlabel('Time (Hours)')
plt.ylabel('Energy (MWh)')
plt.title('Optimized Energy Mix')
plt.legend()
plt.show()
