import matplotlib.pyplot as plt
from matplotlib import ticker
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
pressures = np.logspace(-8, -4, 20) * 1e2

io_power = [1e3]
ex_powers = [1e6]
powers = np.vstack((io_power, ex_powers)).T

phio = Phio()
phio.medium.set_excitation_params(ex_order, ex_cs_SI)
phio.medium.set_ionization_params(io_order, io_cs_SI)

io = Laser()
io.geometry.set_parallel_beam(1e-3)
ex = Laser()
ex.geometry.set_parallel_beam(1e-3)

fig, ax = plt.subplots()

for ip, ep in powers:
    I = []
    mfp = []
    for p in pressures:
        phio.medium.set_conditions(p, temperature)
        phio.medium.set_gas_params(2.18e-25, 396e-12)

        io.set_cw(532e-9, ip)
        ex.set_cw(249.6e-9, ep)
        phio.rempi.define_lasers(ex, io)
        phio.rempi.calculate_parameters()

        phio.rempi.continuous(method="BDF")
        print(f"completed run p: {p}.")

        I.append(phio.rempi.average_current())
        mfp.append(phio.medium.mean_free_path)

    ax.loglog(mfp, I, 'k-', label=f'{ep}, {ip}')
ax.set_xlabel("Mean free path [m]")
ax.set_ylabel("Current [A]")
ax.grid(which="both")
plt.show()