import matplotlib.pyplot as plt
import numpy as np

from phio.phio import Phio
from phio.laser.laser import Laser

order = 3
cs = 4.6e-83
cs_SI = cs * 1e-2**(2*order)
temperature = 150 + 273.15
pressure = 1e-6 * 1e2

num_rep = 5

pulse_energies = np.logspace(-12, 0, 14)

fig, ax = plt.subplots(1, 2)

phio = Phio()
phio.medium.set_conditions(pressure, temperature)
phio.medium.set_gas_params(2.18e-25)
phio.medium.set_ionization_params(order, cs_SI)

l1 = Laser()
l1.load_laser("lasers_config/Nd:YAG-4.yaml")
l1.geometry.load_geometry("lasers_config/Nd:YAG-4.yaml")
l2 = Laser()
l2.load_laser("lasers_config/Nd:YAG-4.yaml")
l2.geometry.load_geometry("lasers_config/Nd:YAG-4.yaml")

pc1 = []
pc2= []

for pe in pulse_energies:
    l1.pulse_energy = pe

    phio.mpi.define_lasers(l1)
    phio.mpi.calculate_parameters(verbose=True)
    phio.mpi.pulse(method="BDF")
    print(phio.mpi.peak_current())
    pc1.append(phio.mpi.peak_current())
    
    l2.pulse_energy = pe
    phio.mpi.calculate_parameters(verbose=True)
    phio.mpi.pulse(method="BDF")
    pc2.append(phio.mpi.peak_current())

ax[0].loglog(pulse_energies, pc1, label=pe)
ax[1].loglog(pulse_energies, pc2, label=pe)
ax[0].grid()
ax[1].grid()
plt.show()

"""for pe in pulse_energies:
    io.set_pulsed(193e-9, pe, 25e-9, 150)
    io.geometry.set_focused_beam(5.5e-6, 190e-3, 10e-3)

    phio.mpi.define_lasers(io)
    phio.mpi.calculate_parameters(verbose=True)
    t, N = phio.mpi.repetition(number_repetitions=num_rep, method="BDF")

    ac.append(phio.mpi.average_current())

    ax[0,1].plot(t, N[1], label=pe)
ax[0,1].grid()
ax[0,1].set_xlim(t[0], t[-1])
ax[0,1].set_ylim(np.min(N))
#ax[0,1].legend()
ax[0,1].set_xlabel("Time [s]")
ax[0,1].set_title(f"Population change over {num_rep} repetitions")

ax[1,0].loglog(pulse_energies, pc)
ax[1,0].grid(which="both")
ax[1,1].loglog(pulse_energies, ac)
ax[1,1].grid(which="both")

plt.show()"""