from phio.phio import Phio

phio = Phio()
phio.laser.create_pulsed(wavelength=249.6e-9, pulse_energy=3e-3, pulse_duration=5e-9, repetition_rate=150)
phio.laser.define_parallel_geo(beam_diameter=1e-3)

print(phio.laser.__dict__)

# Or

from phio.laser import Laser

laser = Laser()
laser.create_pulsed(wavelength=249.6e-9, pulse_energy=3e-3, pulse_duration=5e-9, repetition_rate=150)
laser.define_parallel_geo(beam_diameter=1e-3)
phio.set_laser(laser_obj=laser)

print(phio.laser.__dict__)