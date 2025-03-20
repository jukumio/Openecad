SketchPlane0 = add_sketchplane(
	origin= [0., 0., 0.], normal= [1., 0., 0.], x_axis= [ 0.,  1., -0.], y_axis= [0., 0., 1.])
Loops0 = []
Curves0_0 = []
Circle0_0_0 = add_circle(center= [175.5, 128. ], radius= 47.5)
Curves0_0.append(Circle0_0_0)
Loop0_0 = add_loop(Curves0_0)
Loops0.append(Loop0_0)
Curves0_1 = []
Circle0_1_0 = add_circle(center= [175.5, 128. ], radius= 25.175)
Curves0_1.append(Circle0_1_0)
Loop0_1 = add_loop(Curves0_1)
Loops0.append(Loop0_1)
Profile0 = add_profile(Loops0)
Sketch0 = add_sketch(sketch_plane= SketchPlane0, profile= Profile0,
	sketch_position= [-0.  , -0.75,  0.  ], sketch_size= 1.5)
Extrude0 = add_extrude(sketch= Sketch0,
	operation= 0, type= 0, extent_one= 0.15, extent_two= 0.)
