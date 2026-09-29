from scipy.integrate import solve_ivp
import numpy as np

from .utils import calculate_kinetic_rate, calculate_photon_flux

PLANCK_CONST = 6.62607015e-34
LIGHT_SPEED = 299792458.0
ELEMENTARY_CHARGE = 1.60217663e-19

class REMPI:
    def __init__(self, medium):
        self.medium = medium

    def define_lasers(self, excitation_laser, ionization_laser):
        self.excitation_laser = excitation_laser
        self.ionization_laser = ionization_laser

    def calculate_parameters(self, reversible_decay_rate=0, irreversible_decay_rate=0, verbose=False):
        self.min_volume = min(self.excitation_laser.geometry.ionization_volume, self.ionization_laser.geometry.ionization_volume)
        initial_particle_number = self.min_volume * self.medium.number_density
        self.N = [initial_particle_number, 0, 0]

        excitation_photon_flux = calculate_photon_flux(self.excitation_laser.peak_power,
                                                        self.excitation_laser.wavelength,
                                                        self.excitation_laser.geometry.spot_area)
        ionization_photon_flux = calculate_photon_flux(self.ionization_laser.peak_power,
                                                        self.ionization_laser.wavelength,
                                                        self.ionization_laser.geometry.spot_area)

        self.k0 = excitation_photon_flux ** self.medium.excitation_order * self.medium.excitation_cross_section
        self.k1 = ionization_photon_flux ** self.medium.ionization_order * self.medium.ionization_cross_section

        self.min_area = min(self.excitation_laser.geometry.ionization_region_area, self.ionization_laser.geometry.ionization_region_area)

        self.k2 = reversible_decay_rate
        self.gamma = irreversible_decay_rate

        if verbose:
            print(f"Excitation photon flux: {excitation_photon_flux:.2e}")
            print(f"Ionization photon flux: {ionization_photon_flux:.2e}")
            print(f"Excitation rate: {self.k0:.2e}")
            print(f"Ionization rate: {self.k1:.2e}")
            print(f"Reversible decay rate: {self.k2:.2e}")
            print(f"Irreversible decay rate: {self.gamma:.2e}")

    def pulse(self, t_eval=None, method="RK45"):
        initial_state = self.N.copy()
        res = solve_ivp(self._pulse_derivatives, [0, self.ionization_laser.pulse_duration], initial_state, t_eval=t_eval, method=method)

        self.pulse_time_array = res.t
        self.pulse_population_array = res.y

        return res.t, res.y

    def repetition(self, number_repetitions=2, n_eval=20, method="RK45"):
        state = self.N.copy()

        all_t = []
        all_y = []

        if self.excitation_laser.repetition_rate != self.ionization_laser.repetition_rate:
            raise ValueError(f" Excitation repetition rate: {self.excitation_laser.repetition_rate} and ionization repetition rate {self.ionization_laser.repetition_rate} must be equal!")
        if self.excitation_laser.pulse_duration != self.ionization_laser.pulse_duration:
            raise ValueError(f" Excitation pulse duration: {self.excitation_laser.pulse_duration} and ionization pulse duration {self.ionization_laser.pulse_duration} must be equal!")
        
        rep_time = 1 / self.ionization_laser.repetition_rate

        for i in range(number_repetitions):
            t_start = i * rep_time
            t_pulse_end = t_start + self.ionization_laser.pulse_duration
            t_end = (i + 1) * rep_time

            t_eval_on = np.linspace(t_start, t_pulse_end, n_eval)

            res_on = solve_ivp(self._pulse_derivatives, [t_start, t_pulse_end], state, t_eval=t_eval_on, method=method)

            if not res_on.success:
                raise ValueError(f"IVP solution failed: {res_on.message} Try decreasing parameters.")

            state = res_on.y[:, -1]

            t_eval_off = np.linspace(t_pulse_end, t_end, n_eval)

            res_off = solve_ivp(self._repetition_derivatives_off, [t_pulse_end, t_end], state, t_eval=t_eval_off, method=method)

            if not res_off.success:
                raise ValueError(f"IVP solution failed: {res_off.message} Try decreasing parameters.")

            state = res_off.y[:, -1]

            all_t.extend([res_on.t, res_off.t])
            all_y.extend([res_on.y, res_off.y])

        self.repetition_time_array = np.concatenate(all_t)
        self.repetition_population_array = np.concatenate(all_y, axis=1)

        return np.concatenate(all_t), np.concatenate(all_y, axis=1)
    
    def _pulse_derivatives(self, t, state):
        N0, N1, N2 = state

        kr = calculate_kinetic_rate(N0,
                                    self.min_area,
                                    self.medium.mean_speed,
                                    self.min_volume,
                                    self.medium.number_density)

        dN0 = -self.k0 * (N0 - N1) + self.k2 * N1 + kr
        dN1 = self.k0 * (N0 - N1) - self.k2 * N1 - self.gamma * N1 - self.k1 * N1
        dN2 = self.k1 * N1

        return dN0, dN1, dN2

    def _repetition_derivatives_off(self, t, state):
            N0, N1, N2 = state
    
            kr = calculate_kinetic_rate(N0,
                                        self.min_area,
                                        self.medium.mean_speed,
                                        self.min_volume,
                                        self.medium.number_density)
    
            dN0 = self.k2 * N1 + kr
            dN1 = - self.k2 * N1 - self.gamma * N1
            dN2 = 0
    
            return dN0, dN1, dN2

    def continuous(self, n_eval=20, method="RK45", t_end=1):
        state = self.N.copy()

        t_eval = np.linspace(0, t_end, n_eval)

        res = solve_ivp(self._pulse_derivatives, [0, t_end], state, t_eval=t_eval, method=method)
        
        if not res.success:
            raise ValueError(f"IVP solution failed: {res.message} Try decreasing parameters.")

        self.cw_time_array = res.t
        self.cw_population_array = res.y

        return res.t, res.y

    def peak_current(self, arrays=None, verbose=False):
        if arrays:
            time_array, population_array = arrays
        else:
            time_array = self.pulse_time_array
            population_array = self.pulse_population_array
        rate = population_array[-1][-1] / time_array[-1]
        current = rate * ELEMENTARY_CHARGE

        if verbose: print(f"PeaK current: {current:.2e} A")

        return current

    def average_current(self, arrays=None, verbose=False):
        if arrays:
            time_array, population_array = arrays
        else:
            if self.ionization_laser.type == "pulsed":
                time_array = self.repetition_time_array
                population_array = self.repetition_population_array
            elif self.ionization_laser.type == "cw":
                time_array = self.cw_time_array
                population_array = self.cw_population_array
            else: raise ValueError(f"Unknown laser type: {self.ionization_laser.type}.")
        rate = population_array[-1][-1] / time_array[-1]
        current = rate * ELEMENTARY_CHARGE

        if verbose: print(f"Average current: {current:.2e} A")

        return current