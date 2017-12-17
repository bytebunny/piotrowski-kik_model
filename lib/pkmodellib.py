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
import scipy.interpolate as spi
import scipy.integrate as spint
import matplotlib.pyplot as plt
# local library specific imports:



def getProfiles(rail_path='', wheel_path=''):
    """Returns rail and wheel profiles from given paths.

    If no path is given, returns empty array.

    Input:
    rail_path -- string with path to rail profile.
    wheel_path -- string with path to wheel profile.

    /Rostyslav Skrypnyk
    """
    rail = []
    if rail_path:
        rail = np.loadtxt(rail_path)
        rail[:,1] = - rail[:,1] # Point z-axis upwards.
    
    wheel = []
    if wheel_path:
        wheel = np.loadtxt(wheel_path, skiprows=2)
        wheel[:,1] = - wheel[:,1] # Point z-axis upwards.

    return rail, wheel
# End function getProfiles.


def plotProfiles(profile1, profile2=[], contact_point=[]):
    """Plots profile(s).

    Input:
    profile1 -- 2d array of coordinates in solid blue.
    profile2 (optional) -- 2d array of coordinates in dashed red.

    /Rostyslav Skrypnyk
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel('$y$, [mm]')
    plt.ylabel('$z$, [mm]')

    ax.plot(profile1[:,0], profile1[:,1], 'b-')

    if len(profile2) != 0:
        ax.plot(profile2[:,0], profile2[:,1], 'r--')

    if len(contact_point) != 0:
        ax.plot(contact_point[0], contact_point[1], 'ko')

    plt.tight_layout() # Adjust margins to fit tick and axis labels, and titles.
    plt.show()
# End of function plotProfiles.


def equalPoints(profile1, profile2):
    """Returns interpolated profile1 with same number of points as in profile2.

    Input:
    profile1 --  2d array of coordinates to be modified.
    profile2 --  reference 2d array of coordinates.

    /Rostyslav Skrypnyk
    """
    itp = spi.interp1d(profile1[:,0], profile1[:,1], kind='linear')

    return np.array([profile2[:,0], itp(profile2[:,0])]).T
# End of function equalPoints.


def separationOfProfiles(wheel, rail):
    """Returns distance between points of two profiles f(y).

    Profiles need to be defined in a common coordinate system. The top profile
    (wheel) needs to be the first one in the list of arguments.

    Input:
    wheel --  2d array of coordinates.
    rail --  2d array of coordinates.

    /Rostyslav Skrypnyk
    """
    sep = wheel[:,1] - rail[:,1]

    # Correct separation if profiles overlap or do not touch:
    min_sep = min(sep)

    return sep - min_sep
# End of function separationOfProfiles.


def interpenetration(wheel, rail, delta0):
    """Returns values interpenetration function.

    The interpenetration function is defined by eq. 7 in the original article.

    Input:
    wheel -- 2d array of coordinates.
    rail -- 2d array of coordinates.
    delta0 - virtual penetration.

    /Rostyslav Skrypnyk
    """
    sep = separationOfProfiles(wheel, rail)

    interp_array = delta0 - sep

    ind = 0
    for interp in interp_array:
        if interp > 0:
            interp_array[ind] = interp
        else:
            interp_array[ind] = 0
        ind += 1

    return interp_array
# End of function interpenetration.


def nonzeroRuns(a):
    """Returns (n,2) array where n is number of runs of non-zeros.

    The first column is the index of the first non-zero in each run,
    and the second is the index of the first zero element after the run.
    This indexing pattern matches, for example, how slicing works and how
    the range function works.

    Input:
    a -- 1d array.

    /Rostyslav Skrypnyk
    """
    # Create an array that's 1 where a isn't 0, and pad each end with an extra 0.
    notzero = np.concatenate(([0], np.not_equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(notzero)) # Calculate a[n+1] - a[n] for all.
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges
# End of function nonzeroRuns.


def maxPressure(wheel, g_array, radius, E, nu, delta, delta0):
    """Returns array of maximum pressures for all contact patches.

    Each entry of the returned array is an evaluated eq. 13 in
    the original article.

    Input:
    wheel -- 2d array of coordinates of the wheel.
    g_array -- interpenetration array.
    radius -- wheel nominal rolling radius.
    E -- Young's modulus.
    nu -- Poisson's ratio.
    delta -- penetration.
    delta0 -- virtual penetration.

    /Rostyslav Skrypnyk
    """
    y_array, z_array = wheel[:,0], wheel[:,1]
    coef = 0.5 * np.pi * E * delta / (1. - nu * nu)

    # Function to compute x coordinate of the front edge of the
    # interpenetration region using in situ rolling radius:
    x_front_edge = lambda ind: np.sqrt(2. * radius * g_array[ind])

    # 1st integrand:
    f1 = lambda x,y,ind: np.sqrt(x_front_edge(ind) ** 2 - x * x) / \
                         np.sqrt(x * x + y * y + 1.e-10)
    # 2nd integrand:
    f2 = lambda x,ind: np.sqrt(x_front_edge(ind) ** 2 - x * x)

    # Identify regions with positive interpenetration function:
    region_array = nonzeroRuns(g_array)

    pmax_array = []
    for region in region_array:
        ind_l, ind_u = region[0], region[1]
        int2_f1 = 0
        int2_f2 = 0
        for ind in range(ind_l, ind_u):
            x_f = x_front_edge(ind)
            int2_f1 += spint.quad(lambda x: f1(x,y_array[ind],ind),
                                  - x_f, x_f,
                                  limit=100)[0]
            int2_f2 += spint.quad(lambda x: f2(x,ind),
                                  - x_f, x_f)[0]

        load = coef / int2_f1 * int2_f2
        pmax = load * np.sqrt(2. * radius * delta0) / int2_f2
        pmax_array.append(pmax)
            
    return np.array(pmax_array)
# End of function maxPressure.
