# PhyberSIM: Brain Fiber Bundle Simulator

## Overview
This code implements a brain fiber bundle simulator using spline curves for fiber representation.

## Prerequisites
- The code has been executed on both Windows and Ubuntu platforms.
- Tested on Python 3.9.

## Code Dependencies
To use the code, install the following libraries:
- [Numpy](https://numpy.org/)
- [Geomdl](https://pypi.org/project/geomdl/)
- [Scipy](https://www.scipy.org/)

### Dependency installation on Windows and Ubuntu
- pip3 install numpy
- pip3 install geomdl
- pip3 install scipy


## Example
In the following folder are available resampled centroids with 21 points.

## Whole-brain datasets
In the following folder are available three simulated whole brain datasets.

## Input parameters
- **centroids**: Centroids in format .bundles/.bundlesdata. The default path is the example folder. (Fibers must have 21 points).
- **r1_range, r2_range, r3_range, r4_range, r5_range**: Range radii of the 5 cross-sections.
- **numb_fib_total_range**: Range for the total number of fibers per simulated bundle.
- **mu, sigma_range**: Mean and variance to optionally add Gaussian noise to the first 5 points at each end of the fiber.

## Output files
All output files are stored in the results folder:
- **Simulated_tractography.bundles/.bundlesdata**: Contains all the simulated resulting clusters together in .bundles/.bundlesdata format.
- **Parameters.txt**: Contains stored tuples of the values of the radii sections and the number of fibers for each simulated bundle.
- **labels.txt**: Contains the labels of the fibers belonging to each simulated bundle.
