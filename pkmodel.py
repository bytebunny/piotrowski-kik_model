"""Implementation of Piotrowski-Kik contact model.

Details and references about the model can be found in README.

Convention.
In the following code the adopted naming convention is the one of PEP 8
(see https://www.python.org/dev/peps/pep-0008/#naming-conventions) with
the exception that the function and method names are mixedCase. 

/Rostyslav Skrypnyk
"""

# Standard library imports:

# 3rd party imports:
import numpy as np
# local library specific imports:
import settings as s
import pkmodellib as pkl

def main():
    rail = np.loadtxt(s.rail_path)
    rail[:,1] = - rail[:,1] # Point z-axis upwards.

    wheel = np.loadtxt(s.wheel_path, skiprows=2)
    wheel[:,1] = - wheel[:,1] # Point z-axis upwards.
    
    pkl.plotProfiles(rail, wheel)

# End of function main.



# Make sure main() does not run when the file is being imported:
if __name__ == '__main__':
    main()

