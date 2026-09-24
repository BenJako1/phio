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

pulse_energies = np.logspace(-3, -1, 3)

fig, ax = plt.subplots(1, 2)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_ionization_params(order, cs_SI)

io = Laser()

for pe in pulse_energies:
    io.set_pulsed(193e-9, pe, 25e-9, 150)
    io.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

    phio.mpi.define_lasers(io)
    phio.mpi.calculate_parameters(verbose=True)
    t, N = phio.mpi.pulse(method="BDF")

    ax[0].plot(t, N[1], label=pe)
ax[0].grid()
ax[0].set_xlim(t[0], t[-1])
ax[0].set_ylim(np.min(N), np.max(N))
ax[0].set_xlabel("Time [s]")
ax[0].set_ylabel("Population")
ax[0].legend()
ax[0].set_title("Population change over pulse")

for pe in pulse_energies:
    io.set_pulsed(193e-9, pe, 25e-9, 150)
    io.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

    phio.mpi.define_lasers(io)
    phio.mpi.calculate_parameters(verbose=True)
    t, N = phio.mpi.repetition(number_repetitions=num_rep, method="BDF")

    ax[1].plot(t, N[1], label=pe)
ax[1].grid()
ax[1].set_xlim(t[0], t[-1])
ax[1].set_ylim(np.min(N))
ax[1].legend()
ax[1].set_xlabel("Time [s]")
ax[1].set_title(f"Population change over {num_rep} repetitions")

phio.mpi.average_current(verbose=True)
phio.mpi.peak_current(verbose=True)

plt.show()