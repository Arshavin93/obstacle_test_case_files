# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:10:29 2024

@author: visha
"""

import rasterio
import numpy as np
from rasterio.transform import Affine
import matplotlib.pyplot as plt
import csv

# Define grid parameters with fixed cell sizes
cell_size_x = 0.0028
cell_size_y = 0.0028
x = np.linspace(-0.098, 1.75, 660)
y = np.linspace(-0.06, 1.06, 400)
X, Y = np.meshgrid(x, y)

# Polynomial equation for the base surface
def polynomial_z(x):
    return 0.1086 * (x**4) - 0.5179 * (x**3) + 1.3434 * (x**2) - 1.6513 * x + 0.8923

# Calculate Z-values using the polynomial equation
Z = polynomial_z(X)

# Cylinder parameters
radius = 0.0186
height = 0.1

# First row: 7 cylinders
centers_row1 = [(0.5217, 0.2375, 0.3299), (0.5217, 0.325, 0.3299), (0.5217, 0.4125, 0.3299), (0.5217, 0.5, 0.3299), (0.5217, 0.5875, 0.3299), (0.5217, 0.675, 0.3299), (0.5217, 0.7625, 0.3299)]
# Second row: 8 cylinders, staggered
centers_row2 = [(0.6792, 0.1954, 0.2503), (0.6792, 0.2829, 0.2503), (0.6792, 0.3704, 0.2503), (0.6792, 0.4579, 0.2503), (0.6792, 0.5454, 0.2503), (0.6792, 0.6329, 0.2503), (0.6792, 0.7204, 0.2503), (0.6792, 0.8079, 0.2503)]
# Third row: 9 cylinders, staggered
centers_row3 = [(0.8367, 0.15, 0.200), (0.8367, 0.2375, 0.200), (0.8367, 0.325, 0.200), (0.8367, 0.4125, 0.200), (0.8367, 0.5, 0.200), (0.8367, 0.5875, 0.200), (0.8367, 0.675, 0.200), (0.8367, 0.7625, 0.200), (0.8367, 0.85, 0.200)]

# Function to add a cylinder to the surface
def add_cylinder(Z, center_x, center_y, radius, height, base_z):
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    cylinder_mask = dist_from_center <= radius
    Z_cylinder = np.zeros_like(Z)
    Z_cylinder[cylinder_mask] = base_z + height
    return np.maximum(Z, Z_cylinder)

# Add all cylinders to the surface
Z_combined = Z.copy()
for center_x, center_y, base_z in centers_row1 + centers_row2 + centers_row3:
    Z_combined = add_cylinder(Z_combined, center_x, center_y, radius, height, base_z)
# Create affine transformation
transform = Affine.translation(x[0] - cell_size_x / 2, y[0] - cell_size_y / 2) * Affine.scale(cell_size_x, cell_size_y)

# Write to GeoTIFF file
with rasterio.open('./array_cylinder_obstacles_height_01.tif', 'w', driver='GTiff', height=Z_combined.shape[0], width=Z_combined.shape[1], count=1, dtype='float32', crs='EPSG:32643', transform=transform) as dst:
    dst.write(Z_combined, 1)

