import numpy as np

BOLTZMANN_CONST = 1.380649e-23

class Medium:
    def __init__(self):
        pass

    def set_conditions(self, pressure, temperature):
        self.pressure = pressure
        self.temperature = temperature

        self.number_density = pressure / (BOLTZMANN_CONST * temperature)

    def set_excitation_params(self, order, cross_section):
            self.excitation_order = order
            self.excitation_cross_section = cross_section

    def set_ionization_params(self, order, cross_section):
        self.ionization_order = order
        self.ionization_cross_section = cross_section

    def set_gas_params(self, atomic_mass):
        self.atomic_mass = atomic_mass

        self.mean_speed = np.sqrt(8 * BOLTZMANN_CONST * self.temperature / (np.pi * self.atomic_mass))
