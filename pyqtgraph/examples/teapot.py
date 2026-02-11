import sys
from pathlib import Path
import numpy as np
import pyqtgraph as pg
from pyqtgraph.opengl import GLViewWidget, GLScatterPlotItem
import trimesh
import OpenGL

print(pg.__version__)
print(pg.Qt.VERSION_INFO)
print(sys.version)
print(np.__version__)
print(OpenGL.__version__)


path = Path(__file__).parent / "Utah_teapot_solid.stl"

mesh = trimesh.load(str(path), allow_remote=True)
mesh.apply_translation(-mesh.bounds.mean(axis=0))

dist = (mesh.extents**2).sum()**0.5

pos = np.ascontiguousarray(mesh.vertices, dtype=np.float32)
color = np.zeros((len(pos), 4), dtype=np.float32)
color[:, :3] = (mesh.vertex_normals + 1.0) * 0.5
color[:, 3] = 0.5

pg.mkQApp()
win = GLViewWidget()
win.setCameraPosition(distance=dist)
spitem = GLScatterPlotItem(pos=pos, color=color, size=0.1, pxMode=False)
win.addItem(spitem)
win.show()
pg.exec()