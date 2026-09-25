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

pulse_powers = np.logspace(0, 7, 15)

fig, ax = plt.subplots()

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_ionization_params(order, cs_SI)

io = Laser()

ac = []
for pp in pulse_powers:
    io.set_cw(193e-9, pp)
    io.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

    phio.mpi.define_lasers(io)
    phio.mpi.calculate_parameters()
    phio.mpi.continuous(method="BDF")

    ac.append(phio.mpi.average_current())

ax.loglog(pulse_powers, ac)

ax.legend()
ax.grid(which="both")
plt.show()