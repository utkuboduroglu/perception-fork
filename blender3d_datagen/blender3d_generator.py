# This tool is to generate datasets from fix parameters with Blender
# for configs, use a .blend file, and probably also a .json file
# TODO: instead of passing parameters to these methods, just pass config object

import bpy
import mathutils
import sys
import numpy as np
import json

def loadConfig(filename, mode='r'):
    with open(filename, mode) as filep:
        data = json.load(filep)
        return data

def polarToCartesian(rad, ang):
    # x := rad * cos (ang) - rad * sin (ang)
    # y := rad * sin (ang) + rad * cos (ang)
    return (
        rad*np.cos(ang) - rad*np.sin(ang),
        rad*np.sin(ang) + rad*np.cos(ang)
    )

def createCollection(context, contextName):
    object_collection = bpy.data.collections.new(contextName)
    global_collection = context.scene.collection

    global_collection.children.link(object_collection)
    return object_collection

def spawnCamera(context):
    # we can generate new cameras with the following
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)

    camera_object.rotation_mode = 'QUATERNION'
    camera_object.rotation_quaternion = mathutils.Quaternion((.1, .2, .1, .2))

    context.scene.collection.objects.link(camera_object)


# TODO: Add parameter for specifying mesh
def generateRandomTuples(objectCountinScene):
    # during random generation, maybe specify the FOV of our camera(s)
    # for occlusion and not including bounding boxes that cannot be drawn on the image
    randGen = np.random.default_rng()
    randomSamples = np.random.rand(objectCountinScene * 2)
    randomPositions = randGen.choice(randomSamples, size=(objectCountinScene, 2), replace=False)

    return randomPositions

def randomToXYZ(points, maxRange, clampRange):
    list(filter(lambda x: clampRange[0] <= x[1] <= clampRange[1], points))
    cartesianPos = [polarToCartesian(p[0], p[1]*2*np.pi) for p in points]

    # TODO: clamping coordinates do not work
    objectPositions = [maxRange * (np.array([p[0], p[1], 0])) for p in cartesianPos]
    return objectPositions


# clampRange allows us to specify angle range to insert meshes in, multiplied by 2pi
def projectedTupleToMeshes(positions, context, clampRange=None):
    if clampRange is None:
        clampRange = [0, 1]

    max_radius = 10

    objectPositions = randomToXYZ(positions, max_radius, clampRange)

    # prevent collisions while generating
    # every object has a bounding box, check for collisions by considering intersections in these

    global_collection = bpy.context.scene.collection
    object_collection = createCollection(bpy.context, 'Objects')

    for pos in objectPositions:
        # adding primitives automatically changes the active object to the mesh created
        bpy.ops.mesh.primitive_cylinder_add(location=pos)

        object_collection.objects.link(context.active_object)
        global_collection.objects.unlink(context.active_object)

        context.active_object.select_set(False)

if __name__ == '__main__':
    # generate random triples in R^3 up to number of desired objects
    # and project them onto the xy-plane
    objectCountinScene = 10
    datagenConfig = loadConfig('/home/utku/Projects/Perception/cfg/blender3d_datagen_config.json')

    spawnCamera(bpy.context)
    randomPositions = generateRandomTuples(datagenConfig['3d_space_object_parameters']['max_objects_in_scene'])
    projectedTupleToMeshes(randomPositions, bpy.context,
                           datagenConfig['3d_space_object_parameters']['object_radial_interval'])
