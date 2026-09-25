PLANCK_CONST = 6.62607015e-34
LIGHT_SPEED = 299792458.0

def calculate_photon_flux(power, wavelength, spot_area):
    photon_energy = PLANCK_CONST * LIGHT_SPEED / wavelength
    intensity = power / spot_area
    photon_flux = intensity / photon_energy

    return photon_flux

def calculate_kinetic_rate(number_particles, ionization_region_area, mean_speed, ionization_volume, number_density):
    kinetic_rate = ionization_region_area * mean_speed * (number_density - number_particles / ionization_volume) / 4

    return kinetic_rate