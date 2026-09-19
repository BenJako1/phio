import numpy as np

k_B = 1.380649e-23
h = 6.62607015e-34
c = 299792458.0
e = 1.60217663e-19

class Process:
    def __init__(self, sim_obj):
        self.sim_obj = sim_obj

    def pulse_current(self):
        particle_number = self.sim_obj.laser.ionization_volume * self.sim_obj.medium.number_density

        photon_energy = h * c / self.sim_obj.laser.wavelength
        intensity = self.sim_obj.laser.pulse_power / self.sim_obj.laser.spot_area
        photon_flux = intensity / photon_energy

        ionization_rate = self.sim_obj.medium.number_density * self.sim_obj.medium.cross_section * photon_flux**self.sim_obj.medium.order

        current = ionization_rate * e

        return current