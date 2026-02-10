"""This example demonstrates the use of GLPointsItem."""

import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.opengl.items.GLPointsItem import GLPointsItem

## Create a GL View widget to display data
app = pg.mkQApp("GLPointsItem Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLPointsItem')
w.setCameraPosition(distance=50)

## Add a grid to the view
g = gl.GLGridItem()
g.scale(2,2,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
w.addItem(g)

## Saddle example with x and y specified
nx, ny = 20, 20
x = np.linspace(-8, 8, nx)
y = np.linspace(-8, 8, ny)
z = 0.1 * ((x.reshape(ny,1) ** 2) - (y.reshape(1,nx) ** 2))
surface = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='normalColor',
                          showGrid=True, lineColor=(0.25,0.25,0.25,1))
w.addItem(surface)

# create data points from x, y, z for GLPointsItem
data = np.empty((x.size * y.size, 3), dtype=np.float32)
data[:, 0] = np.repeat(x, y.size)
data[:, 1] = np.tile(y, x.size)
data[:, 2] = z.flatten()

points = GLPointsItem(
    pos=data,
    color=(1.0, 0.0, 0.0, 1.0),
    size=4.0
)
w.addItem(points)

if __name__ == '__main__':
    pg.exec()
