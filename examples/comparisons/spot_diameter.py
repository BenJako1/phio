import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

order = 2
cs = 1.1e-51
cs_SI = cs * 1e-2**(2*order)
temperature = 150 + 273.15
pressure = 1e-6 * 1e2

ps = np.logspace(-6, -3, 50)
es = np.logspace(-6, 0, 7)

fig, ax = plt.subplots(2, 1)

for e in es:
    ac = []
    pc = []
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
        phio.mpi.pulse(method="BDF")
        phio.mpi.repetition(number_repetitions=1, method="BDF")

        ac.append(phio.mpi.average_current())
        pc.append(phio.mpi.peak_current())

    ax[0].loglog(ps, pc, label=f"{e:.0e}")
    ax[1].loglog(ps, ac, label=f"{e:.0e}")
#ax.legend(title="Pulse energy [J]")
#ax.grid(which="both")
#ax.set_xlabel("Spot diameter [m]")
#ax.set_ylabel("Number of ionizations")
plt.show()