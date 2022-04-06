from geovista import Transform
from geovista.geoplotter import GeoPlotter
from geovista import theme
from iris import load_cube
from iris.experimental.ugrid import PARSE_UGRID_ON_LOAD
from iris.tests import get_data_path

file_path = get_data_path(["NetCDF", "unstructured_grid", "lfric_surface_mean.nc"])

with PARSE_UGRID_ON_LOAD.context():
    my_cube = load_cube(file_path, "zh")

face_node = my_cube.mesh.face_node_connectivity
lons, lats = my_cube.mesh.node_coords
indices = face_node.indices_by_location()
my_polydata = Transform.from_unstructured(
    lons.points,
    lats.points,
    indices,
    data=my_cube.data[0],
    start_index=face_node.start_index,
    name=my_cube.name(),
)
my_polydata.save(f"{my_cube.name()}.vtk")

my_plotter = GeoPlotter()
my_plotter.theme.font.color = (0.5,) * 3
my_plotter.add_coastlines()
my_plotter.add_mesh(my_polydata)
my_plotter.camera.zoom(4)
my_plotter.show()
