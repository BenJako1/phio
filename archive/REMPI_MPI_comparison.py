import numpy as np
import matplotlib.pyplot as plt

from archive.rate_mfp import RateMfp
from utils.draw_pressure_isolines import draw_pressure_isolines
from utils.labellines import labelLines

pressure = np.logspace(-7, -4, 4)
temperature = 150 # C

pulse_energy = [4e-3]  # J
pulse_duration = 35e-12  # s
wavelength = 266  # nm

spot_diameter = 0.01 # mm
focal_length = 190  # mm
aperture_diameter = 10  # mm

order = 3
cross_section = 6.2e-83
kinetic_diameter = 396e-12

# CONSTANTS
e = 1.60217663e-19

fig, ax = plt.subplots(1, 2, figsize=(10, 5), layout='constrained')
lines = []

sim = RateMfp()
sim.background_medium(
    pressure_mbar=pressure,
    temperature_C=temperature,
    cross_section_cm=cross_section,
    kinetic_diameter_m=kinetic_diameter,
    order=order,
)

for pe in pulse_energy:
    sim.laser(
        pe,
        pulse_duration,
        aperture_diameter,
        wavelength,
        focused=True,
        spot_diameter_mm=spot_diameter,
        focal_length_mm=focal_length,
    )

    rate, mfp = sim.calculate_rate_mfp()
    #rate = sim.calculate_cw_rate()

    current_uA = rate * e * 1e6

    # Main mean-free-path curve
    line, = ax[0].loglog(
        mfp,
        current_uA,
        color='black',
        label=f'{pe*1e3:.1f} mJ f',
        marker='x'
    )

    lines.append(line)

ax[0].set_xlim()

# Pressure isolines
draw_pressure_isolines(
    ax[0],
    mean_free_paths=mfp,
    pressures_mbar=pressure,
    direction='vertical'
)

ax[0].grid(True, which="both")
ax[0].set_ylabel('Current [$\\mu$A]')
ax[0].set_xlabel('Mean free path [m]')

sim.background_medium(
    pressure_mbar=pressure,
    temperature_C=temperature,
    cross_section_cm=4e-45,
    kinetic_diameter_m=kinetic_diameter,
    order=2,
)

wavelength = 249.6
aperture_diameter = 1 # mm

lines = []

for pe in pulse_energy:
    sim.laser(
        pe,
        pulse_duration,
        aperture_diameter,
        wavelength,
        focused=False
    )

    rate, mfp = sim.calculate_rate_mfp()
    #rate = sim.calculate_cw_rate()

    current_uA = rate * e * 1e6

    # Main mean-free-path curve
    line, = ax[1].loglog(
        mfp,
        current_uA,
        color='black',
        label=f'{pe*1e3:.1f} mJ',
        marker='x'
    )

    lines.append(line)

ax[1].set_xlim()

# Pressure isolines
draw_pressure_isolines(
    ax[1],
    mean_free_paths=mfp,
    pressures_mbar=pressure,
    direction='vertical'
)

ax[1].grid(True, which="both")
ax[1].set_ylabel('Current [$\\mu$A]')
ax[1].set_xlabel('Mean free path [m]')

plt.show()