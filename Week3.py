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
vol = table["col3"]

#Constants
mass_blackhole = 3e7 * au.solMass

#Create initial chart from input data, set labels
plt.plot(dis, vol)
plt.xlabel("Distance (kp/c)")
plt.ylabel("Velocity (km/s)")

#Calculates orbital velocity given Mass and Radius
def calculate_orbital_velocity(M, r):
    ret_val = np.sqrt((ac.G * M) / r)
    return ret_val

vel_ret = np.zeros(np.shape(dis)) * au.km / au.s

for i, radius in enumerate(dis):
    radius_with_units = radius * 1000 * au.parsec
    orb_velocity = calculate_orbital_velocity(mass_blackhole, radius_with_units)
    print(f'The orbital velocity at radius {radius} is {orb_velocity.to(au.km / au.s)}')
    vel_ret[i] = orb_velocity

#Plot black hole data
plt.plot(vel_ret, color = 'red', label = 'With only Supermassive Black Hole')
plt.show()