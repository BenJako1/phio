from .laser.laser import Laser
from .medium import Medium
from .process import Process
from .population import MPI, REMPI

class Phio:
    def __init__(self):
        self.laser = Laser()
        self.medium = Medium()
        self.process = Process(self.laser, self.medium)

        self.mpi = MPI(self.medium)
        self.rempi = REMPI(self.medium)

    def set_laser(self, laser_obj):
        self.laser = laser_obj

    def set_medium(self, medium_obj):
        self.medium = medium_obj

    