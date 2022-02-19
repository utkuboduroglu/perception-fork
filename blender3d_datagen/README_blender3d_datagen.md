This is a reference document for writing well-defined Blender3D datagen config files.

## `3d_space_object_parameters`
This setting is for changing how objects rendered in the scene will act.
* `object_max_dist` [`float`]: How far any object can be from the world origin.
* `object_rand_dist_type`: What type of distribution should be used for generating random coordinates for objects to be placed.
Options include:
  * `inverse_square`, `gaussian`, `uniform`.
* `max_objects_in_scene` [`int`]
* `object_radial_interval` [`float`, `float`]: The interval of angles for which objects should be placed in between.
Measured in radians ranging from `[-pi, pi]`.
* `prevent_collisions` [`bool`]: Whether we want to check for mesh collisions before placing them down; a simple bounding-box check.

## `object_visual_details`
A setting for adding variation to the visual details of objects being placed, like textures, materials, size etc.
* `object_color_type`: Specifies which color our objects should be. Options include:
  * `yellow`, `blue`, `mixed`, `misc`
* `object_yellow_dist` [`float`]: The probability of any given placed cone to be `yellow`.
* `object_blue_dist` [`float`]: The probability of any given placed cone to be `blue`. 
Note that these two parameters need not add up to 1, to account for `misc` cones, although `P(mixed) = P(yellow) + P(blue)`.
* `object_size_variation` [`float`]

## `3d_space_camera_parameters`
Parameters to influence the variations in camera placement and angles.
* `camera_height_dist` [`float`]: Factor to change camera height, relative scale.
* `camera_vert_angle_dist` [`float`]: Factor to change vertical camera angle, relative scale.
* `camera_hor_angle_dist` [`float`]: Factor to change horizontal camera angle, relative scale.
* `camera_location` [`vec3::<float>`]: 3D vector for camera location.

## `3d_space_visual_parameters`
Parameters to influence the visual elements of the scene, like lighting conditions, scene type etc.
* `illumination_level_kelvin` [`float`]: The light intensity of the sun-object, measured in blackbody temperature.
* `sun_intensity` [`float`]: The intensity of the sun relative to the real sun.
* `scene_time_of_day_GMT` [`int`]: The time of day in the scene, specified as a 24hr 4-digit integer, w.r.t. GMT.

## `3d_scene_misc_objects`
A list of objects to be inserted into the scene regardless of the above parameters. The general format of objects should follow:
* `name`: Name of object to be used in Blender.
* `type`: Type of object to be created. Options are:
  * `cone_mesh`, `camera`, `light_source`.
* `location`: The desired location of the object.
* `rot_??`: The desired rotation of the object. This parameter can be specified with 2 different names, namely
    * `rot_euler` and `rot_quaternion`.