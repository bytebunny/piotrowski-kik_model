"""Library of routines for Piotrowski-Kik contact model.

Convention.
In the following code the adopted naming convention is the one of PEP 8
(see https://www.python.org/dev/peps/pep-0008/#naming-conventions) with
the exception that the function and method names are mixedCase. 

/Rostyslav Skrypnyk
"""

# Standard library imports:

# 3rd party imports:
import numpy as np
import matplotlib.pyplot as plt
# local library specific imports:



def plotProfiles(profile1, profile2=[]):
    """Plots profile(s)

    Input:
    profile1 -- 2d array of x,y pairs in solid blue.
    profile2 (optional) -- 2d array of x,y pairs in dashed red.

    /Rostyslav Skrypnyk
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel('$y$, [mm]')
    plt.ylabel('$z$, [mm]')

    ax.plot(profile1[:,0], profile1[:,1], 'b-')

    if len(profile2) != 0:
        ax.plot(profile2[:,0], profile2[:,1], 'r--')

    plt.tight_layout() # Adjust margins to fit tick and axis labels, and titles.
    plt.show()
# End of function plotProfiles.
