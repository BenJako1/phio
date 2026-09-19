import numpy as np

def calculate_rate_mfp_rempi(
    pressure_mbar,
    radius_mm,
    temperature_C,
    order,
    sigma_cm,
    intensity_MW_cm2,
    wavelength_nm,
    d_K_m
):
    # Constants
    k_B = 1.380649e-23  # Boltzmann constant [J K^-1]
    h = 6.62607015e-34  # Planck constant [J s]
    c = 299792458.0  # Speed of light [m s^-1]

    pressure_Pa = pressure_mbar * 100
    radius_m = radius_mm * 1e-3
    temperature_K = temperature_C + 273.15
    if temperature_K <= 0:
        raise ValueError("Temperature must be above absolute zero.")
    intensity_W_m2 = intensity_MW_cm2 * 1e10
    wavelength_m = wavelength_nm * 1e-9

    # Cross section unit conversion
    sigma_exponent = 2 * order
    sigma_SI = sigma_cm * (1e-2) ** sigma_exponent

    # Volume
    volume_m3 = 4.0 / 3.0 * np.pi * radius_m**3

    # Number of particles
    n = pressure_Pa / (k_B * temperature_K)
    n_particles = n * volume_m3

    # Photon energy
    photon_energy_J = h * c / wavelength_m

    # Photon flux
    photon_flux = intensity_W_m2 / photon_energy_J

    # Rate
    rate = n_particles * sigma_SI * photon_flux**order

    # Mean free path
    mfp = 1 / (np.pi * d_K_m ** 2 * n)

    return rate, mfp