from .laser import Laser
from .medium import Medium
from .process import Process

class Phio:
    def __init__(self):
        self.laser = Laser()
        self.medium = Medium()
        self.process = Process(self)

    def set_laser(self, laser_obj):
        self.laser = laser_obj

    def set_medium(self, medium_obj):
        self.medium = medium_obj

    