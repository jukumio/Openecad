 Of course, here are the codes:
```python
SketchPlane0 = add_sketchplane(
	origin= [0., 0., 0.], normal= [ 0., -1.,    0.], x_axis= [ 1.,    0., -0.], y_axis= [0., 0., 1.])
Loops0 = []
Curves0_0 = []
Circle0_0_0 = add_circle(center= [175.5, 128. ], radius= 47.5)
Curves0_0.append(Circle0_0_0)
Loop0_0 = add_loop(Curves0_0)
Loops0.append(Loop0_0)
Curves0_1 = []
Circle0_1_0 = add_circle(center= [175.5, 128. ], radius= 38.)
Curves0_1.append(Circle0_1_0)
Loop0_1 = add_loop(Curves0_1)
Loops0.append(Loop0_1)
Profile0 = add_profile(Loops0)
Sketch0 = add_sketch(sketch_plane= SketchPlane0, profile= Profile0,
	sketch_position= [-0.75, -0.   ,    0.    ], sketch_size= 1.5)
Extrude0 = add_extrude(sketch= Sketch0,
	operation= 0, type= 0, extent_one= 0.375, extent_two= 0.)
SketchPlane1 = add_sketchplane(
	origin= [0., 0., 0.], normal= [ 0., -1.,    0.], x_axis= [ 1.,    0., -0.], y_axis= [0., 0., 1.])
Loops1 = []
Curves1_0 = []
Circle1_0_0 = add_circle(center= [175.5, 128. ], radius= 47.5)
Curves1_0.append(Circle1_0_0)
Loop1_0 = add_loop(Curves1_0)
Loops1.append(Loop1_0)
Curves1_1 = []
Circle1_1_0 = add_circle(center= [175.5, 128. ], radius= 38.)
Curves1_1.append(Circle1_1_0)
Loop1_1 = add_loop(Curves1_1)
Loops1.append(Loop1_1)
Profile1 = add_profile(Loops1)
Sketch1 = add_sketch(sketch_plane= SketchPlane1, profile= Profile1,
	sketch_position= [-0.75, -0.   ,    0.    ], sketch_size= 1.5)
Extrude1 = add_extrude(sketch= Sketch1,
	operation= 1, type= 0, extent_one= 0.375, extent_two= 0.)
```
