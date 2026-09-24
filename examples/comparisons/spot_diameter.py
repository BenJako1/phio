import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

#ELEMENTARY_CHARGE = 1.60217663e-19

order = 2
cs = 1.1e-51
cs_SI = cs * 1e-2**(2*order)
temperature = 150 + 273.15
pressure = 1e-6 * 1e2

ps = np.logspace(-6, -3, 50)
es = np.logspace(-3, 0, 4)

fig, ax = plt.subplots(1, 1)

for e in es:
    Ns = []
    for p in ps:
        io = Laser()
        io.set_pulsed(193e-9, e, 25e-9, 150)
        io.geometry.set_focused_beam(p, 190e-3, 10e-3)

        phio = Phio()
        phio.medium.set_conditions(pressure, temperature)
        phio.medium.set_gas_params(2.18e-25)
        phio.medium.set_ionization_params(order, cs_SI)

        phio.mpi.define_lasers(io)
        phio.mpi.calculate_parameters()
        t, N = phio.mpi.pulse(method="BDF")

        Ns.append(N[1][-1])

    ax.loglog(ps, Ns, label=f"{e:.0e}")
ax.legend(title="Pulse energy [J]")
ax.grid(which="both")
ax.set_xlabel("Spot diameter [m]")
ax.set_ylabel("Number of ionizations")
plt.show()