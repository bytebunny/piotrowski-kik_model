"""Implementation of Piotrowski-Kik contact model.

Details and references about the model can be found in README.

Convention.
In the following code the adopted naming convention is the one of PEP 8
(see https://www.python.org/dev/peps/pep-0008/#naming-conventions) with
the exception that the function and method names are mixedCase. 

/Rostyslav Skrypnyk
"""

# Standard library imports:
import sys
sys.path.insert(0, './lib') # Add lib to path.
# 3rd party imports:
import numpy as np
# local library specific imports:
import settings as s
import pkmodellib as pkl
import geometry as geom

def main():
    rail, wheel = pkl.getProfiles(s.rail_path, s.wheel_path)
    new_wheel = pkl.equalPoints(wheel, rail)

    interpen = pkl.interpenetration(new_wheel, rail,
                                    s.virtual_penetration)
    max_pressures = pkl.maxPressure(new_wheel, interpen,
                                    s.wheel_radius, s.E, s.nu,
                                    s.penetration, s.virtual_penetration)
    print max_pressures
# End of function main.



# Make sure main() does not run when the file is being imported:
if __name__ == '__main__':
    main()

