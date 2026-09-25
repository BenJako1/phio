from .laser.laser import Laser
from .medium import Medium
from .rempi import REMPI
from .mpi import MPI

class Phio:
    def __init__(self):
        self.laser = Laser()
        self.medium = Medium()

        self.mpi = MPI(self.medium)
        self.rempi = REMPI(self.medium)

    def set_laser(self, laser_obj):
        self.laser = laser_obj

    def set_medium(self, medium_obj):
        self.medium = medium_obj

    