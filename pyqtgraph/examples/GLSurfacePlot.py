"""
This example demonstrates the use of GLSurfacePlotItem.
"""
import sys

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore

if 'darwin' in sys.platform:
    fmt = QtGui.QSurfaceFormat()
    fmt.setRenderableType(fmt.RenderableType.OpenGL)
    fmt.setProfile(fmt.OpenGLContextProfile.CoreProfile)
    fmt.setVersion(4, 1)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)

## Create a GL View widget to display data
app = pg.mkQApp("GLSurfacePlot Example")
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
w.setCameraPosition(distance=50)

## Add a grid to the view
g = gl.GLGridItem()
g.scale(2,2,1)
g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
w.addItem(g)


## Simple surface plot example
## x, y values are not specified, so assumed to be 0:50
z = pg.gaussianFilter(np.random.normal(size=(50,50)), (1,1))
p1 = gl.GLSurfacePlotItem(z=z, shader='shaded', color=(0.5, 0.5, 1, 1), showGrid=True)
p1.scale(16./49., 16./49., 1.0)
p1.translate(-18, 2, 0)
w.addItem(p1)


## Saddle example with x and y specified
x = np.linspace(-8, 8, 50)
y = np.linspace(-8, 8, 50)
z = 0.1 * ((x.reshape(50,1) ** 2) - (y.reshape(1,50) ** 2))
p2 = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='normalColor',
                          showGrid=True, lineColor=(0.25,0.25,0.25,1))
p2.translate(-10,-10,0)
w.addItem(p2)


## Manually specified colors
z = pg.gaussianFilter(np.random.normal(size=(50,50)), (1,1))
x = np.linspace(-12, 12, 50)
y = np.linspace(-12, 12, 50)
colors = np.ones((50,50,4), dtype=np.float32)
colors[...,0] = np.clip(np.cos(((x.reshape(50,1) ** 2) + (y.reshape(1,50) ** 2)) ** 0.5), 0, 1)
colors[...,1] = colors[...,0]

p3 = gl.GLSurfacePlotItem(z=z, colors=colors.reshape(50*50,4), shader='shaded', smooth=False)
p3.scale(16./49., 16./49., 1.0)
p3.translate(2, -18, 0)
w.addItem(p3)


## Torus surface with 2D x, y coordinates and grid enabled
nx, ny = 25, 25
u = np.linspace(0, 2*np.pi, nx)
v = np.linspace(0, 2*np.pi, ny)
u_grid, v_grid = np.meshgrid(u, v, indexing='ij')

# Torus parametric equations
R = 3.0  # major radius
r = 1.0  # minor radius
x_torus = (R + r * np.cos(v_grid)) * np.cos(u_grid)
y_torus = (R + r * np.cos(v_grid)) * np.sin(u_grid)
z_torus = r * np.sin(v_grid)

# Create torus colors based on v parameter
colors_torus = np.ones((nx, ny, 4), dtype=np.float32)
colors_torus[..., 0] = np.cos(v_grid) * 0.5 + 0.5  # Red channel
colors_torus[..., 1] = np.sin(u_grid) * 0.5 + 0.5  # Green channel
colors_torus[..., 2] = 0.7                          # Blue channel

p4_torus = gl.GLSurfacePlotItem(x=x_torus, y=y_torus, z=z_torus, colors=colors_torus,
                                shader='normalColor', showGrid=True, lineColor=(1, 1, 1, 0.5),
                                lineWidth=0.5)
p4_torus.translate(-10, -10, 8)
w.addItem(p4_torus)


## Animated example
## compute surface vertex data
cols = 90
rows = 100
x = np.linspace(-8, 8, cols+1).reshape(cols+1,1)
y = np.linspace(-8, 8, rows+1).reshape(1,rows+1)
d = (x**2 + y**2) * 0.1
d2 = d ** 0.5 + 0.1

## precompute height values for all frames
phi = np.arange(0, np.pi*2, np.pi/20.)
z = np.sin(d[np.newaxis,...] + phi.reshape(phi.shape[0], 1, 1)) / d2[np.newaxis,...]


## create a surface plot, tell it to use the 'heightColor' shader
## since this does not require normal vectors to render (thus we 
## can set computeNormals=False to save time when the mesh updates)
p5 = gl.GLSurfacePlotItem(x=x[:,0], y = y[0,:], shader='heightColor', computeNormals=False, smooth=False)
p5.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
p5.translate(10, 10, 0)
w.addItem(p5)

index = 0
def update():
    global p5, z, index
    index -= 1
    p5.setData(z=z[index%z.shape[0]])
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)

if __name__ == '__main__':
    pg.exec()
