import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

ex_order = 2
ex_cs = 6e-18
ex_cs_SI = ex_cs * 1e-2**(2*ex_order)
io_order = 1
io_cs = 4e-45
io_cs_SI = io_cs * 1e-2**(2*io_order)
temperature = 150 + 273.15
pressure = 1e-6 * 1e2

ex = Laser()
ex.set_pulsed(249.6e-9, 3e-5, 25e-9, 150)
ex.geometry.set_parallel_beam(1e-3)

io = Laser()
io.set_pulsed(249.6e-9, 3e-5, 25e-9, 150)
io.geometry.set_parallel_beam(1e-3)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_excitation_params(ex_order, ex_cs_SI)
phio.medium.set_ionization_params(io_order, io_cs_SI)

phio.rempi.define_lasers(ex, io)
phio.rempi.calculate_parameters()

print(phio.rempi.k0, phio.rempi.k1, phio.rempi.k)

t, N = phio.rempi.pulse(method="BDF")

plt.plot(t, N[2], label="ion")
plt.plot(t, N[1], label="ex")
plt.plot(t, N[0], label="base")
plt.legend()
plt.grid()
plt.show()