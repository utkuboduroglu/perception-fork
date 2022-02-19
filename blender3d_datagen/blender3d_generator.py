# This tool is to generate datasets from fix parameters with Blender
# for configs, use a .blend file, and probably also a .json file

import bpy
import mathutils
import sys
import numpy as np


def spawnCamera(context):
    # we can generate new cameras with the following
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    context.scene.collection.objects.link(camera_object)


# TODO: Add parameter for specifying mesh
def generateRandomTuple(objectCountinScene):
    # during random generation, maybe specify the FOV of our camera(s)
    # for occlusion and not including bounding boxes that cannot be drawn on the image
    randGen = np.random.default_rng()
    randomSamples = np.random.rand(objectCountinScene * 2)
    randomPositions = randGen.choice(randomSamples, size=(objectCountinScene, 2), replace=False)

    return randomPositions

def projectedTupleToMeshes(positions, context):
    objectPositions = [10 * (np.array([p[0], p[1], 0.5]) - 0.5) for p in positions]

    # prevent collisions while generating
    # every object has a bounding box, check for collisions by considering intersections in these

    for pos in objectPositions:
        # adding primitives automatically changes the active object to the mesh created
        bpy.ops.mesh.primitive_cube_add(location=pos)
        context.active_object.select_set(False)

if __name__ == '__main__':
    # generate random triples in R^3 up to number of desired objects
    # and project them onto the xy-plane
    objectCountinScene = 10

    spawnCamera(bpy.context)
    randomPositions = generateRandomTuple(objectCountinScene)
    projectedTupleToMeshes(randomPositions, bpy.context)
