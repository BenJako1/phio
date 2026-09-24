from scipy.integrate import solve_ivp
import numpy as np

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

        excitation_photon_flux = _calculate_photon_flux(self.excitation_laser.peak_power,
                                                        self.excitation_laser.wavelength,
                                                        self.excitation_laser.geometry.spot_area)
        ionization_photon_flux = _calculate_photon_flux(self.ionization_laser.peak_power,
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

    def _pulse_derivatives(self, t, state):
        N0, N1, N2 = state

        kr = _calculate_kinetic_rate(N0,
                                    self.min_area,
                                    self.medium.mean_speed,
                                    self.min_volume,
                                    self.medium.number_density)

        dN0 = -self.k0 * (N0 - N1) + self.k2 * N1 + kr
        dN1 = self.k0 * (N0 - N1) - self.k2 * N1 - self.gamma * N1 - self.k1 * N1
        dN2 = self.k1 * N1

        return dN0, dN1, dN2

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

            print(f"state before res_on: {state}")

            print(self.k0, self.k1, self.k2, self.gamma)

            print(t_start, t_pulse_end)

            res_on = solve_ivp(self._repetition_derivatives_on, [t_start, t_pulse_end], state, method=method)

            print("success:", res_on.success)

            print("status:", res_on.status)

            print("message:", res_on.message)

            print("t:", res_on.t)

            print("y:", res_on.y)

            print(i, res_on.y)

            state = res_on.y[:, -1]

            t_eval_off = np.linspace(t_pulse_end, t_end, n_eval)

            res_off = solve_ivp(self._repetition_derivatives_off, [t_pulse_end, t_end], state, method=method)

            print(i, res_off.y)

            state = res_off.y[:, -1]

            all_t.extend([res_on.t, res_off.t])
            all_y.extend([res_on.y, res_off.y])

        self.repetition_time_array = np.concatenate(all_t)
        self.repetition_population_array = np.concatenate(all_y, axis=1)

        return np.concatenate(all_t), np.concatenate(all_y, axis=1)
    
    def _repetition_derivatives_on(self, t, state):
        N0, N1, N2 = state

        kr = _calculate_kinetic_rate(N0,
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
    
            kr = _calculate_kinetic_rate(N0,
                                        self.min_area,
                                        self.medium.mean_speed,
                                        self.min_volume,
                                        self.medium.number_density)
    
            dN0 = self.k2 * N1 + kr
            dN1 = - self.k2 * N1 - self.gamma * N1
            dN2 = 0
    
            return dN0, dN1, dN2

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
            time_array = self.repetition_time_array
            population_array = self.repetition_population_array
        rate = population_array[-1][-1] / time_array[-1]
        current = rate * ELEMENTARY_CHARGE

        if verbose: print(f"Average current: {current:.2e} A")

        return current

class MPI:
    def __init__(self, medium):
        self.medium = medium

    def define_lasers(self, ionization_laser):
        self.ionization_laser = ionization_laser

    def calculate_parameters(self,verbose=False):
        initial_particle_number = self.ionization_laser.geometry.ionization_volume * self.medium.number_density
        self.N = [initial_particle_number, 0]

        ionization_photon_flux = _calculate_photon_flux(self.ionization_laser.peak_power,
                                                        self.ionization_laser.wavelength,
                                                        self.ionization_laser.geometry.spot_area)

        self.k1 = ionization_photon_flux ** self.medium.ionization_order * self.medium.ionization_cross_section

        if verbose:
            print(f"Ionization photon flux: {ionization_photon_flux:.2e}")
            print(f"Ionization rate: {self.k1:.2e}")

    def pulse(self, t_eval=None, method="RK45"):
        print(self.k1)
        res = solve_ivp(self._pulse_derivatives, [0, self.ionization_laser.pulse_duration], self.N, t_eval=t_eval, method=method)

        self.pulse_time_array = res.t
        self.pulse_population_array = res.y

        return res.t, res.y

    def _pulse_derivatives(self, t, state):
        N0, N1 = state

        kr = _calculate_kinetic_rate(N0,
                                    self.ionization_laser.geometry.ionization_region_area,
                                    self.medium.mean_speed,
                                    self.ionization_laser.geometry.ionization_volume,
                                    self.medium.number_density)

        dN0 = - self.k1 * N0 + kr
        dN1 = self.k1 * N0

        return dN0, dN1

    def repetition(self, number_repetitions=2, n_eval=20, method="RK45"):
        state = self.N.copy()

        all_t = []
        all_y = []

        rep_time = 1 / self.ionization_laser.repetition_rate

        for i in range(number_repetitions):
            t_start = i * rep_time
            t_pulse_end = t_start + self.ionization_laser.pulse_duration
            t_end = (i + 1) * rep_time

            t_eval_on = np.linspace(t_start, t_pulse_end, n_eval)

            print(self.k1)

            res_on = solve_ivp(self._repetition_derivatives_on, [t_start, t_pulse_end], state, t_eval=t_eval_on, method=method)

            state = res_on.y[:, -1]

            t_eval_off = np.linspace(t_pulse_end, t_end, n_eval)

            res_off = solve_ivp(self._repetition_derivatives_off, [t_pulse_end, t_end], state, t_eval=t_eval_off, method=method)

            state = res_off.y[:, -1]

            all_t.extend([res_on.t, res_off.t])
            all_y.extend([res_on.y, res_off.y])

        self.repetition_time_array = np.concatenate(all_t)
        self.repetition_population_array = np.concatenate(all_y, axis=1)

        return np.concatenate(all_t), np.concatenate(all_y, axis=1)

    def _repetition_derivatives_on(self, t, state):
        N0, N1 = state

        kr = _calculate_kinetic_rate(N0,
                                    self.ionization_laser.geometry.ionization_region_area,
                                    self.medium.mean_speed,
                                    self.ionization_laser.geometry.ionization_volume,
                                    self.medium.number_density)

        dN0 = - self.k1 * N0 + kr
        dN1 = self.k1 * N0

        return dN0, dN1

    def _repetition_derivatives_off(self, t, state):
            N0, N1 = state
    
            kr = _calculate_kinetic_rate(N0,
                                         self.ionization_laser.geometry.ionization_region_area,
                                         self.medium.mean_speed,
                                         self.ionization_laser.geometry.ionization_volume,
                                         self.medium.number_density)
    
            dN0 = kr
            dN1 = 0
    
            return dN0, dN1
    
    def peak_current(self, arrays=None, verbose=False):
        if arrays:
            time_array, population_array = arrays
        else:
            time_array = self.pulse_time_array
            population_array = self.pulse_population_array
        rate = population_array[-1][-1] / time_array[-1]
        current = rate * ELEMENTARY_CHARGE

        if verbose: print(f"Peak current: {current:.2e} A")

        return current

    def average_current(self, arrays=None, verbose=False):
        if arrays:
            time_array, population_array = arrays
        else:
            time_array = self.repetition_time_array
            population_array = self.repetition_population_array
        rate = population_array[-1][-1] / time_array[-1]
        current = rate * ELEMENTARY_CHARGE

        if verbose: print(f"Average current: {current:.2e} A")

        return current

# Helper functions

def _calculate_photon_flux(power, wavelength, spot_area):
    photon_energy = PLANCK_CONST * LIGHT_SPEED / wavelength
    intensity = power / spot_area
    photon_flux = intensity / photon_energy

    return photon_flux

def _calculate_kinetic_rate(number_particles, ionization_region_area, mean_speed, ionization_volume, number_density):
    kinetic_rate = ionization_region_area * mean_speed * (number_density - number_particles / ionization_volume) / 4

    return kinetic_rate