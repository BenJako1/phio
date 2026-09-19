import numpy as np

class RateMfp:
    def __init__(self):
        # Constants
        self.k_B = 1.380649e-23  # Boltzmann constant [J K^-1]
        self.h = 6.62607015e-34  # Planck constant [J s]
        self.c = 299792458.0  # Speed of light [m s^-1]

    def laser(self,
              pulse_energy_J,
              pulse_duration_s,
              aperture_diameter_mm,
              wavelength_nm,
              focused=True,
              **kwargs
              ):
        self.pulse_energy_J = pulse_energy_J
        self.pulse_duration_s = pulse_duration_s
        self.aperture_diameter_m = aperture_diameter_mm * 1e-3
        self.wavelength_m = wavelength_nm * 1e-9
        self.focused = focused

        if focused:
            self.spot_diameter_m = kwargs['spot_diameter_mm'] * 1e-3
            self.focal_length_m = kwargs['focal_length_mm'] * 1e-3

    def background_medium(self,
                          pressure_mbar,
                          temperature_C,
                          cross_section_cm,
                          kinetic_diameter_m,
                          order
                          ):
        self.pressure_mbar = np.array(pressure_mbar)
        self.pressure_Pa = self.pressure_mbar * 1e2
        self.temperature_K = temperature_C + 273.15
        self.cross_section_m = cross_section_cm * (1e-2) ** (2 * order)
        self.kinetic_diameter_m = kinetic_diameter_m
        self.order = order

        if self.temperature_K <= 0:
            raise ValueError("Temperature must be above absolute zero.")

    def calculate_cw_rate(self, atom_mass=2.18e-25):
        number_density__m3 = self.pressure_Pa / (self.k_B * self.temperature_K)
        mean_speed = np.sqrt(8 * self.k_B * self.temperature_K / (np.pi * atom_mass))
        if self.focused:
            area = (2 * np.pi * (self.spot_diameter_m / 2) ** 2 + np.pi * self.spot_diameter_m * 2 *
                    self.spot_diameter_m * self.focal_length_m / self.aperture_diameter_m)
        else:
            area = 4 * np.pi * (self.aperture_diameter_m / 2) ** 2 # surface area of the ionization area

        entry_rate = 0.25 * number_density__m3 * mean_speed * area

        return entry_rate

    def calculate_average_rate(self, frequency):
        rate, mfp = self.calculate_rate_mfp()
        number_electrons = rate * self.pulse_duration_s
        avg_rate = number_electrons * frequency

        return avg_rate, mfp

    def calculate_rate_mfp(self):
        # Power
        pulse_power_W = self.pulse_energy_J / self.pulse_duration_s

        # Mode
        if self.focused:
            volume_m3 = np.pi * self.spot_diameter_m ** 3 * self.focal_length_m / (2 * self.aperture_diameter_m)
        else:
            self.spot_diameter_m = self.aperture_diameter_m
            volume_m3 = 4.0 / 3.0 * np.pi * (self.aperture_diameter_m / 2) ** 3

        # Number of particles
        number_density__m3 = self.pressure_Pa / (self.k_B * self.temperature_K)
        number_particles = number_density__m3 * volume_m3

        # Photon energy and flux
        photon_energy_J = self.h * self.c / self.wavelength_m
        spot_area_m2 = np.pi * (self.spot_diameter_m / 2)**2
        intensity_W__m2 = pulse_power_W / spot_area_m2
        photon_flux__m2s = intensity_W__m2 / photon_energy_J

        # Rate
        rate = number_particles * self.cross_section_m * photon_flux__m2s**self.order

        # Account for maximum rate possible
        for i, out in enumerate(zip(rate, number_particles, self.pressure_mbar)):
            r, N, p = out
            val = r * self.pulse_duration_s
            if val > N:
                print(f"Event exceeds number of particles at pressure = {p} mbar. \n"
                      f"rate = {r:.2e}, req. N = {val:.2e}, N = {N}")
                rate[i] = N / self.pulse_duration_s

        # Mean free path
        mean_free_path = 1 / (np.pi * self.kinetic_diameter_m ** 2 * number_density__m3)

        return rate, mean_free_path

