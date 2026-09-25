import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

order = 2
cs = 1.1e-51
cs_SI = cs * 1e-2**(2*order)
temperature = 150 + 273.15
pressure = 1e-6 * 1e2

num_rep = 5

pulse_energies = np.logspace(-6, 0, 7)
pulse_durations = np.logspace(-9, -6, 7)

fig, ax = plt.subplots(1, 2)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_ionization_params(order, cs_SI)

io = Laser()

for pe in pulse_energies:
    pc = []
    ac = []
    for pd in pulse_durations:
        io.set_pulsed(193e-9, pe, pd, 150)
        io.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

        phio.mpi.define_lasers(io)
        phio.mpi.calculate_parameters()
        print(io.pulse_energy, io.pulse_duration)
        phio.mpi.pulse(method="BDF")
        phio.mpi.repetition(number_repetitions=1, method="BDF")

        ac.append(phio.mpi.average_current())

    ax[0].loglog(pulse_durations, pc, label=pe)
    ax[1].loglog(pulse_durations, ac, label=pe)

ax[0].legend()
ax[0].grid(which="both")
ax[1].legend()
ax[1].grid(which="both")
plt.show()