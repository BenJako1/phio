from phio.phio import Phio
import numpy as np

order = 2
cs = 4e-45
cs_SI = cs * 1e-2**(2*order)

temperature = 150 + 273.15

pressure = 1e-6 * 1e2

phio = Phio()
phio.medium.set_conditions(pressure=pressure,
                           temperature=temperature)
phio.medium.set_ionization_params(order=order,
                                  cross_section=cs_SI)
phio.laser.set_pulsed(wavelength=249.6e-9,
                         pulse_energy=3e-3,
                         pulse_duration=5e-9,
                         repetition_rate=150)
phio.laser.geometry.set_parallel_beam(beam_diameter=1e-3)

peak_current = phio.process.peak_current(verbose=True)
print(peak_current)

avg_current = phio.process.avg_current(verbose=True)
print(avg_current)