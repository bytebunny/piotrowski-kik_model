[//]: # (To preview markdown file in Emacs type C-c C-c p)

# Piotrowski-Kik contact model
Python implementation of [A simplified model of wheel--rail contact mechanics for non-Hertzian problems](http://dx.doi.org/10.1080/00423110701586444).

## Model summary
Semi-Hertzian (semi-elliptical normal pressure distribution along the (rolling) x-axis) non-iterative
contact solution that is particularly usefull when curvatures are not constant along the (lateral)
y-axis. Results shown in the original article are in agreement with results from Kalker's variational
method. However, alike Kalker's method the model is limited to elastic material response and
geometries that permit the assumption of an infinite half-space. Additionally, both bodies
have to possess identical material properties.

## Dependencies
To run the code, you will need the following libraries installed:

- NumPy
- SciPy
- Matplotlib (for visualisation only)

## How to use
1. Place files defining geometry of the profiles in *profiles* directory.
1. In `pkmodel.py`, specify path to the profiles or call functions from
*./lib/*`geometry.py` to work with analytical geometries.
1. Set simulation parameters in `settings.py`.
1. Run `pkmodel.py`.
