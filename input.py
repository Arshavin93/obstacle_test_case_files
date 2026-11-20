sim=TitanSimulation(overwrite_output=True)

sim.setGIS(
    gis_format='GDAL',
    gis_map='/home/arshavin/TITAN2D/analytical_simulation/obstacle_array_of_cylinders/tiff_file/modified_tiffs/array_cylinder_obstacles_height_01_compressed.tif'
)

sim.setScale(
    length_scale=1.65,
    height_scale=1.65,
    gravity_scale=9.8,
)

sim.setNumProp(
    AMR=False,
number_of_cells_across_axis = 46,
    order='Second',
)
sim.setMatModel(
    model='Coulomb',
    int_frict=34.0,
    bed_frict=33.0
)
sim.addPile(
    pile_type='Cylinder',
    height=0.1179,
    center=[0.1, 0.5],
    radii=[0.06113, 0.104],
    orientation=0.0,
    Vmagnitude=0.0,
    Vdirection=0.0,
)


sim.setRestartOutput(
    dtime=0.1,
    diter=None,
    keep_all=False,
    keep_redundant_data=False,
    output_prefix='restart'
)

sim.setTimeProps(
    #max_iter=1000,
    max_time=2.0,
)

sim.setTimeSeriesOutput(
    vizoutput='xdmf',
    dtime=0.1,
)

#start simulation
sim.run()
