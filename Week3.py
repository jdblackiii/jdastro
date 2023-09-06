import numpy as np
import astropy.constants as ac
import astropy.units as au 
import astropy.io.ascii as aio
import matplotlib.pyplot as plt

#Path data will be loaded in from
path = 'galaxy_rotation_2006.txt'
table = aio.read(path)
print(f"Loaded file from {path}\n Loaded data:\n")
print(table)
dis = table["col2"]
vel = table["col3"]

#Constants
mass_blackhole = 3e7 * au.solMass
mass_bulge = 3e10 * au.solMass

#Create initial chart from input data, set labels
plt.plot(dis, vel)
plt.xlabel("Distance (kp/c)")
plt.ylabel("Velocity (km/s)")

#Calculates orbital velocity given Mass and Radius
def calculate_orbital_velocity(M, dis):
    ret_val = np.zeros(np.shape(dis)) * au.km / au.s
    
    for i, radius in enumerate(dis):
        radius_with_units = radius * 1000 * au.parsec
        orb_velocity = np.sqrt((ac.G * M) / radius_with_units)
        print(f'The orbital velocity at radius {radius} is {orb_velocity.to(au.km / au.s)}')
        ret_val[i] = orb_velocity
    return ret_val

#Calculate and plot Black Hole
plt.plot(np.arange(7,35), calculate_orbital_velocity(mass_blackhole, dis), color = 'red', label = 'With only Supermassive Black Hole')

#Calculate and plot Central Bulge
plt.plot(np.arange(7,35), calculate_orbital_velocity(mass_bulge, dis), color = 'purple', label = 'With entire central bulge')

plt.xlim(left = 7)
plt.show()