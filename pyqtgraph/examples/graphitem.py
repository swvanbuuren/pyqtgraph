import pyqtgraph as pg
import pyqtgraph.opengl as gl

pg.mkQApp()

win = gl.GLViewWidget(rotationMethod='quaternion')
win.setCameraPosition(distance=3)

md = gl.MeshData.sphere(rows=20, cols=20)

item = gl.GLGraphItem(
    edges=md.edges(),
    nodePositions=md.vertexes(),
    nodeSize=0.1,
    pxMode=False
)
win.addItem(item)

win.show()
pg.exec()