import numpy as np
import matplotlib.pyplot as plt

from archive.rate_mfp import RateMfp
from utils.labellines import labelLines
from utils.draw_pressure_isolines import draw_pressure_isolines

pressure = [1e-7, 1e-6, 1e-5]
pulse_energy = [4e-3]  # J
pulse_duration = 35e-12  # s

# NON-VARIABLE INPUTS
aperture_diameter = 1 # mm
temperature = 150 # C
order = 2 # order of multiphoton ionization
cross_section = 4e-45 # cm^(2N)s^(N-1) where N is the order
wavelength = 249.6 # nm
kinetic_diameter = 396e-12 # m
frequency = 150 # Hz

kd = [396e-12, 360e-12, 340e-12]

# CONSTANTS
e = 1.60217663e-19

fig, ax = plt.subplots()
lines = []

sim = RateMfp()

for k in kd:
    sim.background_medium(
        pressure_mbar=pressure,
        temperature_C=temperature,
        cross_section_cm=cross_section,
        kinetic_diameter_m=k,
        order=order,
    )
    sim.laser(
        pulse_energy,
        pulse_duration,
        aperture_diameter,
        wavelength,
        focused=False
    )

    rate, mfp = sim.calculate_average_rate(frequency)
    current_uA = rate * e * 1e6

    # Main mean-free-path curve
    line_pulse, = ax.loglog(
        mfp,
        current_uA,
        color='black',
        label=f'',
        marker='x'
    )
    lines.append(line_pulse)

ax.set_xlim()

# Pressure isolines
'''draw_pressure_isolines(
    ax,
    mean_free_paths=mfp,
    pressures_mbar=pressure,
    direction='vertical'
)'''

labelLines(
    lines,
    align=False,
    fontsize=10,
    x_offset=-0.6,
    y_offset=0
)

ax.grid(True, which="both")
ax.set_ylabel('Current [$\\mu$A]')
ax.set_xlabel('Mean free path [m]')

plt.show()