import numpy as np

def calculate_rate_mfp_mpi(
        p_mbar,
       T_C,
       d_mm,
       f_mm,
       D_mm,
       sigma_cm,
       P_p,
       lambda_0_nm,
       K,
       d_K
):
    # CONSTANTS
    k_B = 1.380649e-23
    h = 6.62607015e-34  # Planck constant [J s]
    c = 299792458.0  # Speed of light [m s^-1]

    # Unit conversions
    p = p_mbar * 100
    T = T_C + 273.15
    d = d_mm / 1e3
    f = f_mm / 1e3
    D = D_mm / 1e3
    lambda_0 = lambda_0_nm / 1e9
    sigma_exponent = 2 * K

    sigma_SI = sigma_cm * (1e-2) ** sigma_exponent

    # Volume
    V = np.pi * d ** 3 * f / (2 * D)

    # Number of particles
    n = p / (k_B * T)
    N = n * V

    # Photon flux
    phi = (P_p * lambda_0 / (np.pi * (d/2) ** 2 * h * c))

    print(phi)

    # Rate
    rate = N * sigma_SI * phi ** K

    # Mean free path
    mfp = 1 / (np.pi * d_K**2 * n)

    return rate, mfp