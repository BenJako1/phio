import numpy as np
from pathlib import Path

from phio.config import load_config

class Geometry:
    def __init__(self):
        pass

    def load_geometry(self, filepath):
        geometry_config = load_config(Path(filepath))
        if geometry_config["geometry"] == "focused":
            spot_diameter = float(geometry_config["spot_diameter"])
            focal_length = float(geometry_config["focal_length"])
            aperture_diameter = float(geometry_config["aperture_diameter"])
            self.set_focused_beam(spot_diameter, focal_length, aperture_diameter)
        elif geometry_config["geometry"] == "parallel":
            beam_diameter = float(geometry_config["beam_diameter"])
            self.set_parallel_beam(beam_diameter)
        else:
            raise ValueError(f'Unknown geometry: {geometry_config["geometry"]}')

    def set_focused_beam(self, spot_diameter, focal_length, aperture_diameter):
        self.geometry = "focused"
        self.spot_diameter = spot_diameter
        self.focal_length = focal_length
        self.aperture_diameter = aperture_diameter

        self.ionization_volume = np.pi * self.spot_diameter ** 3 * self.focal_length / (2 * self.aperture_diameter)
        self.spot_area = np.pi * (self.spot_diameter / 2)**2
        self.ionization_region_area = (2 * self.spot_area + np.pi * self.spot_diameter * 2 *
                                       self.spot_diameter * self.focal_length / self.aperture_diameter)
    
    def set_parallel_beam(self, beam_diameter):
        self.geometry = "parallel"
        self.beam_diameter = beam_diameter

        self.ionization_volume = 4 / 3 * np.pi * (self.beam_diameter / 2)**3
        self.spot_area = np.pi * (self.beam_diameter / 2)**2
        self.ionization_region_area = 4 * np.pi * (self.beam_diameter / 2)**2