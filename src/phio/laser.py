import numpy as np

class Laser:
    def __init__(self):
        pass

    def create_cw(self, wavelength, cw_power):
        self.type = "cw"
        self.wavelength = wavelength
        self.cw_power = cw_power

    def create_pulsed(self, wavelength, pulse_energy, pulse_duration, repetition_rate):
        self.type = "pulsed"
        self.wavelength = wavelength
        self.pulse_energy = pulse_energy
        self.pulse_duration = pulse_duration
        self.repetition_rate = repetition_rate

        self.pulse_power = pulse_energy / pulse_duration

    def define_focused_geo(self, spot_diameter, focal_length, aperture_diameter):
        self.geo = "focused"
        self.spot_diameter = spot_diameter
        self.focal_length = focal_length
        self.aperture_diameter = aperture_diameter

        self.ionization_volume = np.pi * self.spot_diameter ** 3 * self.focal_length / (2 * self.aperture_diameter)
        self.spot_area = np.pi * (self.spot_diameter / 2)**2

    def define_parallel_geo(self, beam_diameter):
        self.geo = "parallel"
        self.beam_diameter = beam_diameter

        self.ionization_volume = 4 / 3 * np.pi * (self.beam_diameter / 2)**3
        self.spot_area = np.pi * (self.beam_diameter / 2)**2