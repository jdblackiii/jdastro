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
dis = table["col2"] * 1000 * au.parsec  # Assuming the data is in kpc, converting to parsec
vel = table["col3"] * au.km / au.s

#Constants
mass_blackhole = 3e7 * au.solMass
mass_bulge = 2.3e10 * au.solMass
mass_disk = 2.3e11 * au.solMass
mass_halo = 3.4e11 * au.solMass

radius_disk = 35 * 1000 * au.parsec
radius_halo = 35 * 1000 * au.parsec

#Create initial chart from input data, set labels
plt.plot(dis, vel)
plt.xlabel("Distance (pc)")
plt.ylabel("Velocity (km/s)")

def calculate_orbital_velocity(M, dis, structure_type='point'):
    ret_val = np.zeros(np.shape(dis)) * au.km / au.s
    
    for i, radius in enumerate(dis):
        if structure_type == 'disk':
            # Assuming a uniform disk, the mass interior to radius is proportional to radius^2
            M_effective = M * (radius / radius_disk)**2
        elif structure_type == 'halo':
            # Adjusting the halo's mass distribution assumption
            M_effective = M * (radius / radius_halo)**3
        else:
            # For point masses like black hole and bulge
            M_effective = M
        
        orb_velocity = np.sqrt((ac.G * M_effective) / radius)
        ret_val[i] = orb_velocity.to(au.km / au.s)
    return ret_val

#Plot provided data
plt.plot(dis, vel, color='orange', label='Provided data')

#Calculate and plot Black Hole
black_hole_vels = calculate_orbital_velocity(mass_blackhole, dis, 'point').value
plt.plot(dis, black_hole_vels, color='red', label='Mass of central black hole')

#Calculate and plot Central Bulge
bulge_vels = calculate_orbital_velocity(mass_bulge, dis, 'point').value
plt.plot(dis, bulge_vels, color='purple', label='Mass of central bulge')

#Calculate and plot Disk
disk_vels = calculate_orbital_velocity(mass_disk, dis, 'disk').value
plt.plot(dis, disk_vels, color='green', label='Mass of disk')

#Calculate and plot halo
halo_vels = calculate_orbital_velocity(mass_halo, dis, 'halo').value
plt.plot(dis, halo_vels, color='blue', label='Mass of halo')

#Sum values across all velocity lists
#Combine all lists with zip, then add element wise with list comprehension
sum_vels = [sum(x) for x in zip(black_hole_vels, bulge_vels, disk_vels)]
print(sum_vels)
print(black_hole_vels)

plt.plot(dis, sum_vels, color='blue', label='Mass of all components')


plt.xlim(left=7e3)  # Assuming you want to start from 7 kpc
plt.legend()
plt.show()
