from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

PLANCK_CONST = 6.62607015e-34
LIGHT_SPEED = 299792458.0
ELEMENTARY_CHARGE = 1.60217663e-19

class Population:
    def __init__(self):
        pass

    def define_parameters(self, excitation_rate_param, ionization_rate_param, decay_rev_rate_param=0, decay_irrev_rate_param=0):
        self.k0 = excitation_rate_param
        self.k1 = ionization_rate_param
        self.k2 = decay_rev_rate_param
        self.gamma = decay_irrev_rate_param

    def define_mode(self, mode):
        if mode == "MPI":
            self.N = [0, 1, 0]
        elif mode == "REMPI":
            self.N = [1, 0, 0]
        else: raise ValueError(f"Unknown mode: {mode}")

    def solve(self, t_max, t_eval=None):
        res = solve_ivp(self._derivatives, [0, t_max], self.N, t_eval=t_eval)

        return res.t, res.y

    def _derivatives(self, t, state):
        N0, N1, N2 = state

        dN0 = -self.k0 * (N0 - N1) + self.k2 * N1
        dN1 = self.k0 * (N0 - N1) - self.k2 * N1 - self.gamma * N1 - self.k1 * N1
        dN2 = self.k1 * N1

        return dN0, dN1, dN2

    @staticmethod
    def _calculate_photon_flux(power, wavelength, spot_area):
        photon_energy = PLANCK_CONST * LIGHT_SPEED / wavelength
        intensity = power / spot_area
        photon_flux = intensity / photon_energy

        return photon_flux

    @staticmethod
    def _calculate_kinetic_rate(ionization_region_area, mean_speed, number_density):
        kinetic_rate = 0.25 * ionization_region_area * mean_speed * number_density

        return kinetic_rate

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    pop = Population()

    k1_ls = [1e-1, 1e-2, 1e-3]
    t_max = 100

    for k1 in k1_ls:
        pop.define_parameters(1, k1, 0, 0)
        pop.define_mode("REMPI")
        t, N = pop.solve(t_max, t_eval=np.linspace(0, t_max, 100))
        
        ax[0].plot(t, N[2], label=k1)
        ax[0].plot(t, N[1], '-.', label=k1)

    for k1 in k1_ls:
            pop.define_mode("MPI")
            pop.define_parameters(0, k1, 0, 0)
            t, N = pop.solve(t_max, t_eval=np.linspace(0, t_max, 100))
            ax[1].plot(t, N[2], label=k1)

    ax[0].legend()
    ax[1].legend()
    plt.show()