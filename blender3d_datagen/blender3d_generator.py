# This tool is to generate datasets from fix parameters with Blender
# for configs, use a .blend file, and probably also a .json file
# TODO: instead of passing parameters to these methods, just pass config object

import bpy
import mathutils as mu
import sys
import numpy as np
import json

def loadConfig(filename, mode='r'):
    with open(filename, mode) as filep:
        data = json.load(filep)
        return data

def createCollection(context, contextName):
    object_collection = bpy.data.collections.new(contextName)
    global_collection = context.scene.collection

    global_collection.children.link(object_collection)
    return object_collection

def spawnCameraXYZAngle(context, location, rotation):
    # we can generate new cameras with the following
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)

    camera_object.location = location

    camera_object.rotation_mode = 'XYZ'
    camera_object.rotation_euler = mu.Euler(rotation, 'XYZ')

    context.scene.collection.objects.link(camera_object)


def generateRandomTuples(objectCountinScene):
    return np.random.random_sample((objectCountinScene, 2))

def randomToXYZ(points, maxRange, clampRange):
    # lerp random tuples
    interp_points = [ (maxRange*p[0], 2*np.pi*((clampRange[1]-clampRange[0])*p[1]-clampRange[0]))
                      for p in points ]
    # apply polar to cartesian transformation to tuples
    euclidean_pts = [ (p[0]*np.cos(p[1]), p[0]*np.sin(p[1]), 0.0) for p in interp_points]
    return euclidean_pts


# clampRange allows us to specify angle range to insert meshes in, multiplied by 2pi
def projectedTupleToMeshes(positions, context, clampRange=None):
    if clampRange is None:
        clampRange = (0, 1)

    max_radius = 20

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

    spawnCameraXYZAngle(bpy.context, mu.Vector((5, 5, 5)), mu.Vector((0,0,0)))
    randomPositions = generateRandomTuples(datagenConfig['3d_space_object_parameters']['max_objects_in_scene'])
    projectedTupleToMeshes(randomPositions, bpy.context,
                           datagenConfig['3d_space_object_parameters']['object_radial_interval'])
