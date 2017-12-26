"""Library of routines to generate geometries of bodies in contact.

In the following code the adopted naming convention is the one of
`PEP 8 <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_
with the exception that the function and method names are mixedCase. 

.. module:: geometry

.. moduleauthor:: Rostyslav Skrypnyk
"""

# Standard library imports:
import math
# 3rd party library imports:
import numpy as np
# local library specific imports:


def circularArcPoints(radius, n_points=100, distance=None,
                      orientation_down=True, offset_y=0):
    """Compute coordinates of the circular arc.

    Parameters
    ----------
    radius : float
        radius of the circle.
    n_points : integer
        number of points that constitute the arc (default=100).
    distance : float
        half a span of the arc, i.e. the arc is created on the
        interval [-distance, distance] (default: None, which is later 
        substituted with radius).
    orientation_down : boolean
        orientation of the arc (default: True).
    offset_y : float 
        offset of Y coordinates, [in units of the coordinates]. Used
        for the wheel coordinates and equals to the wheel's radius 
        (default: 0).
    
    Returns
    -------
    2d array
        coordinates of circular arc.
    """
    if distance is None:
        distance = float(radius)
    else: 
        distance = float(distance) # Guard against integer division.
    
    if distance > radius:
        raise ValueError('Half-span of the arc cannot be larger than radius.')
    
    if orientation_down:
        sign = -1
    else:
        sign = 1

    coords = []
    for point in range(n_points+1): # +1 needed to complete the arc.
        # x coordinates from left to right (important for creating sets
        # in Abaqus):
        x = math.cos(math.acos(distance/radius) + 2*math.asin(distance/radius) \
                     * (n_points-point) / n_points)*radius
        y = math.sin(sign*(math.acos(distance/radius) + \
                           2*math.asin(distance/radius)*point/n_points))*radius
        # Offset if orientation_down is True:
        coords.append( (x, y + 0.5*(sign - 1)*(offset_y - radius)) )

    return np.array(coords)

# End of circularArcPoints function.


def ellipticArcPoints(x_axis, y_axis, n_points=100, distance=None,
                      orientation_down=True, offset_y=0):
    """Compute coordinates of the elliptic arc.

    Parameters
    ----------
    x_axis : float
        size of the semi-axis along X.
    y_axis : float
        size of the semi-axis along Y.
    n_points : integer
        number of points that constitute the arc.
    distance : float
        half a span of the arc, i.e. the arc is created on the
        interval [-distance, distance] (default: None, which is later 
        substituted with size of the X semi-axis).
    orientation_down : boolean
        orientation of the arc (default: True).
    offset_y : float
        offset of Y coordinates, [in units of the coordinates]. Used
        for the wheel coordinates and equals to the wheel's radius 
        (default: 0).

    Returns
    -------
    2d array
        coordinates of the elliptic arc.
    """
    if distance is None:
        distance = float(x_axis)
    else: 
        distance = float(distance) # Guard against integer division.
    
    if distance > radius:
        raise ValueError('Half-span of the arc cannot be larger than radius.')
    
    if distance > x_axis:
        raise ValueError( ('Half-span of the arc cannot be ' \
                           'larger than the X semi-axis.') )

    if orientation_down:
        sign = -1
    else:
        sign = 1

    coords = []
    R = math.sqrt( distance**2 + (y_axis**2)*(1 - (distance/x_axis)**2) )
    for point in range(n_points+1): # +1 needed to complete the arc.
        # fraction = (n_points - point) / n_points
        # x coordinates from left to right (important for creating sets
        # in Abaqus):
        fraction = (n_points - point) / float(n_points)
        x = math.cos( math.acos(distance/R) + \
                      2*math.asin(distance/R) * fraction ) * R
        y = sign * y_axis * math.sqrt( 1 - (x/x_axis)**2 )
        coords.append( (x, y + 0.5*(sign - 1)*(offset_y - y_axis)) )

    return np.array(coords)
# End of ellipticArcPoints function.


def rotateGeometry(geometry, angle):
    """Rotate geometry by the specified angle.

    Parameters
    ----------
    geometry : 2d array
        coordinates.
    angle : float 
        angle of rotation in degrees.

    Returns
    -------
    2d array
        rotated geometry.
    """
    theta = (angle/180.) * np.pi
    rotation_matrix = np.array( [[np.cos(theta), -np.sin(theta)],
                                 [np.sin(theta), np.cos(theta)]] )
    rotated_geom = []    
    for point in geometry:
        rotated_geom.append( tuple(np.dot(rotation_matrix, point)) )

    return rotated_geom
# End of rotateGeometry function.
