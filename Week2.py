import numpy as np
import astropy.constants as ac
import astropy.units as au 
import astropy.io.ascii as aio
import matplotlib.pyplot as plt

'''
Orbital velocity equation:
sqrt((G * M) / r)
'''
#Calculating the velocity of the Earth around the Sun:
v_Earth = np.sqrt((ac.G * ac.M_sun) / ac.au)
print(f'Orbital velocity of the Earth around the Sun: {v_Earth.to(au.km / au.s)}\n')

#Calculating orbital velocity of a sattelite around the Earth at sea level
v_orbital = np.sqrt(ac.G * au.earthMass / au.earthRad)
print(f"Orbital velocity of a sattelite at sea level: {v_orbital.to(au.km/ au.s)}\n")

# Calculating Schwarzschild radius of a solar-mass blackhole
rad_bh = ac.G * au.solMass / ac.c ** 2
print(f"Schwarzschild radius of a solar-mass blackhole: {rad_bh.si}\n")

#Path data will be loaded in from
path = '/Users/jdblack/Code/Python/Astronomy/ASTRON1221/DarkMatter/galaxy_rotation_2006.txt'
table = aio.read(path)
print(f"Loaded file from {path}\n Loaded data:\n")
print(table)

dis = table["col2"]
vol = table["col3"]

#Create initial chart from input data, set labels
plt.plot(dis, vol)
plt.xlabel("Distance (kp/c)")
plt.ylabel("Velocity (km/s)")

mass = 3e7 * au.solMass
#rad = 5.68 * 1000 * au.parsec

def calculate_orbital_velocity(M, r):
    ret_val = np.sqrt((ac.G * M) / r)
    return ret_val

vel_ret = np.zeros(np.shape(dis)) * au.km / au.s

'''
Using data loaded in from file, calculate orbital velocity

In this case, we are calculating the orbital velocity of
the milky way if its only mass were the central black hole
'''
for i, radius in enumerate(dis):
    radius_with_units = radius * 1000 * au.parsec
    orb_velocity = calculate_orbital_velocity(mass, radius_with_units)
    print(f'The orbital velocity at radius {radius} is {orb_velocity.to(au.km / au.s)}')
    vel_ret[i] = orb_velocity

#Plot black hole data
plt.plot(vel_ret, color = 'red', label = 'With only Supermassive Black Hole')
plt.show()