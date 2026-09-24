from phio.phio import Phio

filepath = "laser.yaml"

phio = Phio()
phio.laser.load_laser(filepath)

print(phio.laser.__dict__)