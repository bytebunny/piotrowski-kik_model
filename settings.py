"""Settings and parameters associated with implementation of the model.

Convention.
In the following code the adopted naming convention is the one of PEP 8
(see https://www.python.org/dev/peps/pep-0008/#naming-conventions) with
the exception that the function and method names are mixedCase. 

/Rostyslav Skrypnyk
"""

# Standard library imports:

# 3rd party imports:

# local library specific imports:


### Paths:
profiles = './profiles/'
rail_path = profiles + 'uic60i00.rail'
wheel_path = profiles + 'S1002.wheel'

### Material parameters:
E = 183.e3 # Young's modulus, [MPa].
nu = 0.3 # Poisson's ratio, [-].

### Problem settings:
wheel_radius = 460 # Nominal rolling radius, [mm].
virtual_penetration = 1.e-2 # Equivalent penetration in Simpack's language, [mm].
# Ratio between penetration and virtual penetration:
penetration_reduction_factor = 0.55 # < 1.
penetration = virtual_penetration / penetration_reduction_factor
