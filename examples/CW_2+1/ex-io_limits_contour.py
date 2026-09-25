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
pressure = 1e-6 * 1e2

io_powers = np.logspace(0, 3, 50)
ex_powers = np.logspace(0, 6, 50)

X, Y = np.meshgrid(ex_powers, io_powers)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25, 396e-12)
phio.medium.set_excitation_params(ex_order, ex_cs_SI)
phio.medium.set_ionization_params(io_order, io_cs_SI)

io = Laser()
io.geometry.set_parallel_beam(1e-3)
ex = Laser()
ex.geometry.set_parallel_beam(1e-3)

values = np.zeros(Y.shape)

for i, ip in enumerate(io_powers):
    for e, ep in enumerate(ex_powers):
        io.set_cw(532e-9, ip)

        ex.set_cw(249.6e-9, ep)

        phio.rempi.define_lasers(ex, io)
        phio.rempi.calculate_parameters()
        phio.rempi.continuous(method="BDF")
        print(f"completed run ip: {ip}, ep: {ep}.")

        values[i, e] = phio.rempi.average_current()

levels = np.linspace(values.min(), values.max(), 20)
fig, ax = plt.subplots()
cs = ax.contourf(X, Y, values, locator=ticker.LogLocator(), cmap="inferno")
cbar = fig.colorbar(cs)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Excitation power [W]")
ax.set_ylabel("Ionization power [W]")
plt.show()