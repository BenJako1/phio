from phio.phio import Phio

phio = Phio()
phio.medium.set_pt(pressure=1e-3, temperature=300)
print(phio.medium.__dict__)

# Or

from phio.medium import Medium

medium = Medium()
medium.set_pt(pressure=1e-3, temperature=300)
phio.set_medium(medium_obj=medium)
print(phio.medium.__dict__)