import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

order = 3
cs = 1.1e-82
cs_SI = cs * 1e-2**(2*order)
temperature = 150 + 273.15
pressure = 1e-6 * 1e2

io = Laser()
io.set_pulsed(266e-9, 1e1, 25e-9, 150)
io.geometry.set_focused_beam(10e-5, 190e-3, 10e-3)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_ionization_params(2, cs_SI)

phio.mpi.define_lasers(io)
phio.mpi.calculate_parameters()
print(phio.mpi.k1, phio.mpi.k2)
t, N = phio.mpi.pulse(method="BDF")

print(N[1][-1])

plt.plot(t, N[1], label="ion")
plt.plot(t, N[0], label="base")
plt.legend()
plt.grid()
plt.show()