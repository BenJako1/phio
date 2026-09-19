import numpy as np
import matplotlib.pyplot as plt

from utils.labellines import labelLines

# Inputs
atom_mass = 2.18e-25
pressure_Pa = np.array([1e-7, 1e-6, 1e-5, 1e-4]) * 100
temperature_K = 150 + 273.15
aperture_diameter_m = 1e-3
kinetic_diameter_m = [396e-12, 360e-12, 340e-12]
collision_cross_section = 1e-14 / 1e4

# Constants
k_B = 1.380649e-23  # Boltzmann constant [J K^-1]
e = 1.60217663e-19

fig, ax = plt.subplots(1, 2, sharey=True, layout='constrained')

lines_1 = []
lines_2 = []

for k in kinetic_diameter_m:
    number_density__m3 = pressure_Pa / (k_B * temperature_K)
    mean_speed = np.sqrt(8 * k_B * temperature_K / (np.pi * atom_mass))

    area = 4 * np.pi * (aperture_diameter_m / 2) ** 2 # surface area of the ionization region

    mean_free_path = 1 / (np.pi * k ** 2 * number_density__m3)
    #mean_free_path_cs = 1 / (number_density__m3 * collision_cross_section * np.sqrt(2))

    entry_rate = 0.25 * number_density__m3 * mean_speed * area
    current = entry_rate * e

    line, = ax[0].loglog(pressure_Pa/1e2, current, color='black', linestyle='-', label=f"d={k*1e12:.0f} mm")
    lines_1.append(line)
    line, = ax[1].loglog(mean_free_path, current, color='black', linestyle='-', label=f"d={k*1e12:.0f} mm")
    lines_2.append(line)

labelLines(lines_1, align=False, fontsize=10, x_offset=-0.6, y_offset=0)
labelLines(lines_2, align=False, fontsize=10, x_offset=-0.6, y_offset=0)
ax[0].grid(which='both')
ax[1].grid(which='both')
ax[0].set_xlabel("Pressure [mbar]")
ax[1].set_xlabel("Mean free path [m]")
ax[0].set_ylabel("Current [A]")
plt.show()

