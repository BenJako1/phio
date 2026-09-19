import numpy as np
import matplotlib.pyplot as plt

from archive.rate_mfp import calculate_rate_mfp
from utils.draw_pressure_isolines import draw_pressure_isolines
from utils.labellines import labelLines

pressure = np.logspace(-7, -4, 4)
temperature = 150 # C

pulse_energy = 700e-3  # J
pulse_duration = 1e-9  # s
pulse_power = [pulse_energy / pulse_duration]
wavelength = 250  # nm

aperture_diameter = 1  # mm

intensity = pulse_power[0] / (np.pi * (aperture_diameter/2)**2)
print(intensity)

order = 2
cross_section = 4.6e-45
kinetic_diameter = 396e-12

# CONSTANTS
e = 1.60217663e-19

fig, ax = plt.subplots()
currents = []
lines = []

for pp in pulse_power:
    rate, mfp = calculate_rate_mfp(
        pressure,
        temperature,
        pp,
        aperture_diameter,
        wavelength,
        order,
        cross_section,
        kinetic_diameter,
        focused=False
    )

    current_uA = rate * e * 1e6
    currents.append(current_uA)

    # Main mean-free-path curve
    line, = ax.loglog(
        current_uA,
        mfp,
        color='black',
        label=f'{pp/1e6:.1f} MW',
        marker='x'
    )

    lines.append(line)

ax.set_xlim()

# Pressure isolines
draw_pressure_isolines(
    ax,
    mean_free_paths=mfp,
    pressures_mbar=pressure,
    current_uA=currents
)

labelLines(
    lines,
    align=False,
    fontsize=10,
    x_offset=-0.6,
    y_offset=0
)

ax.grid(True, which="both")
ax.set_xlabel('Current [$\\mu$A]')
ax.set_ylabel('Mean free path [m]')

plt.show()