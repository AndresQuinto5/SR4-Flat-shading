#Andrés Emilio Quinto Villagrán - 18288
#Ejercicio: SR4_FLAT

from gl import Render
from gl import color

render = Render()
render.load('cuerpo.obj', translate=(550, 50, 0), scale = (36, 36, 100))
render.glFinish(filename='output.bmp')
