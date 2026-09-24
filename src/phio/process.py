import numpy as np

PLANCK_CONST = 6.62607015e-34
LIGHT_SPEED = 299792458.0
ELEMENTARY_CHARGE = 1.60217663e-19

class Process:
    def __init__(self, laser, medium):
        self.laser = laser
        self.medium = medium

    def peak_current(self, verbose=False):
        if self.laser.type == "pulsed":

            particle_number = self.laser.geometry.ionization_volume * self.medium.number_density

            ionization_rate = (self.medium.number_density *
                                self.medium.cross_section *
                                self._calculate_photon_flux(self.laser.peak_power,
                                                            self.laser.wavelength,
                                                            self.laser.geometry.spot_area) ** self.medium.order)
            
            ionization_rate = self._check_particle_limit(ionization_rate, particle_number, verbose)
            
            current = ionization_rate * ELEMENTARY_CHARGE

        elif self.laser.type == "cw": raise ValueError(f"Laser type cw not compatible with peak current calculation")
        else: raise ValueError(f"Unknown laser type: {self.laser.type}.")
        
        return current

    def avg_current(self, verbose=False):
        particle_number = self.laser.geometry.ionization_volume * self.medium.number_density

        ionization_rate = (self.medium.number_density *
                            self.medium.cross_section *
                            self._calculate_photon_flux(self.laser.avg_power,
                                                        self.laser.wavelength,
                                                        self.laser.geometry.spot_area) ** self.medium.order)

        # This does not work, we cannot use avg_power and then check for particle limit for pulsed
        if self.laser.type == "pulsed":
            ionization_rate = self._check_particle_limit(ionization_rate, particle_number, verbose)
            ionization_rate = ionization_rate * self.laser.repetition_rate
            current = ionization_rate * ELEMENTARY_CHARGE

            time_between_pulses = 1 / self.laser.repetition_rate - self.laser.pulse_duration
            kinetic_rate = self._calculate_kinetic_rate(self.laser.geometry.ionization_region_area, self.medium.mean_speed, self.medium.number_density)
            number_entries = time_between_pulses * kinetic_rate

        elif self.laser.type == "cw":
            kinetic_rate = self._calculate_kinetic_rate(self.laser.geometry.ionization_region_area,
                                                   self.medium.mean_speed,
                                                   self.medium.number_density)
            ionization_rate = self._check_cw_limit(ionization_rate, kinetic_rate)
            current = ionization_rate * ELEMENTARY_CHARGE
            
        else: raise ValueError(f"Unknown laser type: {self.laser.type}.")
        
        return current

    # Helper functions
    def _check_particle_limit(self, ionization_rate, particle_number, verbose):
        if ionization_rate * self.laser.pulse_duration > particle_number:
            if verbose: print(f"Process is particle-limited")
            kinetic_rate = self._calculate_kinetic_rate(self.laser.geometry.ionization_region_area,
                                                        self.medium.mean_speed,
                                                        self.medium.number_density)
            ionization_rate = particle_number / self.laser.pulse_duration + kinetic_rate

        return ionization_rate

    @staticmethod
    def _calculate_photon_flux(power, wavelength, spot_area):
        photon_energy = PLANCK_CONST * LIGHT_SPEED / wavelength
        intensity = power / spot_area
        photon_flux = intensity / photon_energy

        return photon_flux

    @staticmethod
    def _check_cw_limit(ionization_rate, kinetic_rate):
        if ionization_rate < kinetic_rate:
            return ionization_rate
        else:
            return kinetic_rate

    @staticmethod
    def _calculate_kinetic_rate(ionization_region_area, mean_speed, number_density):
        kinetic_rate = 0.25 * ionization_region_area * mean_speed * number_density

        return kinetic_rate