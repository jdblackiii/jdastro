import astropy.units as au
import astropy.constants as ac
import numpy as np

#Radius of solar mass black hole
#Radius of a black hole is derived from velocity equation v = sqrt(G * M / r)
# 2GM / c^2
r_bh = (2 * ac.G * au.solMass) / ac.c ** 2
print(r_bh.to(au.km))

m_bh = (.01 * au.s * ac.c ** 3) / (16 * np.pi * ac.G)
print(m_bh.to(au.solMass))

R_bh = 2 * ac.G * 30 * au.solMass / (ac.c ** 2)
Dist = R_bh / h