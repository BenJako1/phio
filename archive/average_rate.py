import numpy as np
import matplotlib.pyplot as plt

from rate_mfp import RateMfp
from utils.draw_pressure_isolines import draw_pressure_isolines
from utils.labellines import labelLines

pressure = np.logspace(-7, -4, 4)
temperature = 150 # C

pulse_energy = 60e-3  # J
pulse_duration = 25e-9  # s
wavelength = 308  # nm
frequency = [150, 150e3, 150e6] # Hz

spot_diameter = 0.01 # mm
focal_length = 190  # mm
aperture_diameter = 10  # mm

order = 3
cross_section = 6.2e-83
kinetic_diameter = 396e-12

# CONSTANTS
e = 1.60217663e-19

fig, ax = plt.subplots()
currents = []
lines = []

sim = RateMfp()
sim.background_medium(
    pressure_mbar=pressure,
    temperature_C=temperature,
    cross_section_cm=cross_section,
    kinetic_diameter_m=kinetic_diameter,
    order=order,
)

plot_params = [[1, ''], [1e3, 'k'], [1e6, 'M']]

for f, pp in zip(frequency, plot_params):
    sim.laser(
        pulse_energy,
        pulse_duration,
        aperture_diameter,
        wavelength,
        focused=True,
        spot_diameter_mm=spot_diameter,
        focal_length_mm=focal_length,
    )

    rate, mfp = sim.calculate_average_rate(f)

    current_uA = rate * e * 1e6
    currents.append(current_uA)

    # Main mean-free-path curve
    line, = ax.loglog(
        mfp,
        current_uA,
        color='black',
        label=f'{f/pp[0]:.0f} {pp[1]}Hz',
        marker='x'
    )

    lines.append(line)

ax.set_xlim()

# Pressure isolines
draw_pressure_isolines(
    ax,
    mean_free_paths=mfp,
    pressures_mbar=pressure,
    direction='vertical'
)

labelLines(
    lines,
    align=False,
    fontsize=10,
    x_offset=-0,
    y_offset=1
)

ax.grid(True, which="both")
ax.set_ylabel('Current [$\\mu$A]')
ax.set_xlabel('Mean free path [m]')

plt.show()