# This tool is to generate datasets from fix parameters with Blender
# for configs, use a .blend file, and probably also a .json file

import bpy
import mathutils
import sys
import numpy as np

# generate random triples in R^3 up to number of desired objects
# and project them onto the xy-plane
objectNumberinScene = 10
randomPositions = np.random.rand(objectNumberinScene, 2)
objectPositions = [10 * (np.array([p[0], p[1], 0.5]) - 0.5) for p in randomPositions]

# prevent collisions while generating

for pos in objectPositions:
    bpy.ops.mesh.primitive_cube_add(location=pos)
