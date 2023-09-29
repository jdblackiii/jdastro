import numpy as np
import astropy.constants as ac
import astropy.units as au 
import astropy.io.ascii as aio
import matplotlib.pyplot as plt

plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "black",
    "axes.facecolor": "white",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})

#Path data will be loaded in from
path = 'galaxy_rotation_2006.txt'
table = aio.read(path)
print(f"Loaded file from {path}\n Loaded data:\n")
print(table)
dis = table["col2"] * 1000 * au.parsec  # Assuming the data is in kpc, converting to parsec
vel = table["col3"] * au.km / au.s

#Constants
#Source https://www.aanda.org/articles/aa/full_html/2012/10/aa20065-12/T5.html
mass_blackhole = 3e7 * au.solMass
mass_bulge = 4.4e10 * au.solMass
mass_disk = 5.6e10 * au.solMass
mass_halo = 1.3e12 * au.solMass

radius_disk = 200 * 1000 * au.parsec
radius_halo = 200 * 1000 * au.parsec

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
plt.plot(dis, black_hole_vels, color='red', label='Central black hole')

#Calculate and plot Central Bulge
bulge_vels = calculate_orbital_velocity(mass_bulge, dis, 'point').value
plt.plot(dis, bulge_vels, color='purple', label='Central bulge')

#Calculate and plot Disk
disk_vels = calculate_orbital_velocity(mass_disk, dis, 'disk').value
plt.plot(dis, disk_vels, color='green', label='Disk')

#Calculate and plot halo
halo_vels = calculate_orbital_velocity(mass_halo, dis, 'halo').value
plt.plot(dis, halo_vels, color='blue', label='Dark Matter Halo')


#Sum values across all velocity lists
#Combine all lists with zip, then add element wise with list comprehension
sum_vels = [sum(x) for x in zip(black_hole_vels, bulge_vels, disk_vels, halo_vels)]
print(sum_vels)
#print(black_hole_vels)

#sum_no_halo = [sum(x) for x in zip(black_hole_vels, bulge_vels, disk_vels)]

plt.plot(dis, sum_vels, color='black', label='Combined velocity')

#plt.plot(dis, sum_no_halo, color='red', label='Mass without dark matter halo')


#plt.xlim()  # Assuming you want to start from 7 kpc
plt.legend()
plt.show()
