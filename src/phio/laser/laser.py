import numpy as np
from pathlib import Path

from phio.config import load_config
from phio.laser.geometry import Geometry

k_B = 1.380649e-23
h = 6.62607015e-34
c = 299792458.0
e = 1.60217663e-19

class Laser:
    def __init__(self):
        self.geometry = Geometry()

    def load_laser(self, filepath):
        laser_config = load_config(Path(filepath))
        if laser_config["type"] == "pulsed":
            wavelength = float(laser_config["wavelength"])
            pulse_energy = float(laser_config["pulse_energy"])
            pulse_duration = float(laser_config["pulse_duration"])
            repetition_rate = float(laser_config["repetition_rate"])
            self.set_pulsed(wavelength, pulse_energy, pulse_duration, repetition_rate)
        elif laser_config["type"] == "cw":
            wavelength = float(laser_config["wavelength"])
            cw_power = float(laser_config["cw_power"])
            self.set_cw(wavelength, cw_power)
        else:
            raise ValueError(f'Unknown laser type: {laser_config["type"]}')

    def set_cw(self, wavelength, cw_power):
        self.type = "cw"
        self.wavelength = wavelength
        self.cw_power = cw_power

        self.peak_power = cw_power
        self.avg_power = cw_power

    def set_pulsed(self, wavelength, pulse_energy, pulse_duration, repetition_rate):
        self.type = "pulsed"
        self.wavelength = wavelength
        self.pulse_energy = pulse_energy
        self.pulse_duration = pulse_duration
        self.repetition_rate = repetition_rate

        self.peak_power = pulse_energy / pulse_duration
        self.avg_power = pulse_energy * repetition_rate