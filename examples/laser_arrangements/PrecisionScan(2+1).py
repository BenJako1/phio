import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

ex_order = 2
ex_cs = 4e-45 # Kröll et al.
ex_cs_SI = ex_cs * 1e-2**(2*ex_order)
io_order = 1
io_cs = 4.3e-18 # Kröll et al.
io_cs_SI = io_cs * 1e-2**(2*io_order)

temperature = 150 + 273.15
pressure = 1e-6 * 1e2

ps = np.logspace(-6, -3, 50)
es = np.logspace(-3, 0, 4)

fig, ax = plt.subplots(1, 2)

ex = Laser()
ex.set_pulsed(249.6e-9, 5e-6, 25e-9, 150)
ex.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

io = Laser()
io.set_pulsed(550e-9, 1e-4, 25e-9, 150)
io.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_excitation_params(ex_order, ex_cs_SI)
phio.medium.set_ionization_params(io_order, io_cs_SI)

phio.rempi.define_lasers(ex, io)
phio.rempi.calculate_parameters(verbose=True)
t, N = phio.rempi.pulse(method="BDF")

ax[0].plot(t, N[2], 'k-', label="ion")
ax[0].plot(t, N[1], 'k:', label="ex")
ax[0].plot(t, N[0], 'k--', label="base")
ax[0].grid()
ax[0].set_xlim(t[0], t[-1])
ax[0].set_ylim(np.min(N), np.max(N))
ax[0].set_xlabel("Time [s]")
ax[0].set_ylabel("Population")
ax[0].set_title("Population change over pulse")

num_rep = 5
t, N = phio.rempi.repetition(number_repetitions=num_rep, method="BDF")

ax[1].plot(t, N[2], 'k-', label="ion")
ax[1].plot(t, N[1], 'k:', label="ex")
ax[1].plot(t, N[0], 'k--', label="base")
ax[1].grid()
ax[1].set_xlim(t[0], t[-1])
ax[1].set_ylim(np.min(N))
ax[1].legend()
ax[1].set_xlabel("Time [s]")
ax[1].set_title(f"Population change over {num_rep} repetitions")

phio.rempi.average_current(verbose=True)
phio.rempi.peak_current(verbose=True)

plt.show()