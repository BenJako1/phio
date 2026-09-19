from phio.phio import Phio

order = 2
cs = 4e-45
cs_SI = cs * 1e2**(2*order)

phio = Phio()
phio.medium.set_pt(pressure=1e-3, temperature=300)
phio.medium.spec_process(order=order,
                         cross_section=cs_SI)
phio.laser.create_pulsed(wavelength=249.6e-9,
                         pulse_energy=3e-3,
                         pulse_duration=5e-9,
                         repetition_rate=150)
phio.laser.define_parallel_geo(beam_diameter=1e-3)

current = phio.process.pulse_current()

print(current)