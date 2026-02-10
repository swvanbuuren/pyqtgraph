"""
This example demonstrates the use of GLPointsItem.
"""
import sys

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import pyqtgraph.opengl as gl
from pyqtgraph.opengl.items.GLPointsItem import GLPointsItem
from pyqtgraph.Qt import QtCore

if 'darwin' in sys.platform:
    fmt = QtGui.QSurfaceFormat()
    fmt.setRenderableType(fmt.RenderableType.OpenGL)
    fmt.setProfile(fmt.OpenGLContextProfile.CoreProfile)
    fmt.setVersion(4, 1)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)

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
x = np.linspace(-8, 8, 50)
y = np.linspace(-8, 8, 50)
z = 0.1 * ((x.reshape(50,1) ** 2) - (y.reshape(1,50) ** 2))
surface = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='normalColor',
                          showGrid=True, lineColor=(0.25,0.25,0.25,1))
w.addItem(surface)

points = GLPointsItem(
    pos=np.random.randn(1000, 3),
    color=(1.0, 0.0, 0.0, 1.0),
    size=8.0
)
w.addItem(points)

if __name__ == '__main__':
    pg.exec()
