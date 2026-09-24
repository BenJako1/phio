from phio.phio import Phio
import numpy as np

order = 2
cs = 4e-45
cs_SI = cs * 1e-2**(2*order)

temperature = 150 + 273.15

pressure = 1e-6 * 1e2

print("PULSED:")

phio_pulsed = Phio()
phio_pulsed.medium.set_conditions(pressure=pressure,
                           temperature=temperature)
phio_pulsed.medium.set_ionization_params(order=order,
                                  cross_section=cs_SI)
phio_pulsed.medium.set_gas_params(atomic_mass=2.18e-25)
phio_pulsed.laser.geometry.set_parallel_beam(beam_diameter=1e-3)

phio_pulsed.laser.set_pulsed(wavelength=249.6e-9,
                            pulse_energy=3e-3,
                            pulse_duration=5e-9,
                            repetition_rate=150)

peak_current = phio_pulsed.process.peak_current(verbose=True)
print(peak_current)

avg_current = phio_pulsed.process.avg_current(verbose=True)
print(avg_current)

print("CW:")

phio_cw = Phio()
phio_cw.medium.set_conditions(pressure=pressure,
                              temperature=temperature)
phio_cw.medium.set_ionization_params(order=order,
                                     cross_section=cs_SI)
phio_cw.medium.set_gas_params(atomic_mass=2.18e-25)
phio_cw.laser.geometry.set_parallel_beam(beam_diameter=1e-3)

phio_cw.laser.set_cw(wavelength=249.6e-9,
                     cw_power=3e4)

avg_current = phio_cw.process.avg_current(verbose=True)
print(avg_current)

phio_pulsed.population.calculate_parameters("MPI", laser=phio_pulsed.laser)
t, N = phio_pulsed.population.solve()

import matplotlib.pyplot as plt

plt.plot(t, N[2])
plt.plot(t, N[1])
plt.show()