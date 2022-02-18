import bpy
import os

filename = os.path.join(
    os.path.join(os.environ['DRVLSS_PERCEPTION_PATH'], 'blender3d_datagen/'),
    "blender3d_generator.py")
exec(compile(open(filename).read(), filename, 'exec'))