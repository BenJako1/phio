k_B = 1.380649e-23

class Medium:
    def __init__(self):
        pass

    def set_pt(self, pressure, temperature):
        self.pressure = pressure
        self.temperature = temperature

        self.number_density = pressure / (k_B * temperature)

    def spec_process(self, order, cross_section):
        self.order = order
        self.cross_section = cross_section