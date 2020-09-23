#Andres Emilio Quinto Villagran
#Carne 18288
#Laboratorio 3 / OBJ

import struct
from obj import Obj
from collections import namedtuple

V2 = namedtuple("Vertex2", ["x", "y"])
V3 = namedtuple("Vertex3", ["x", "y", "z"])

def sum(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element sum
    """
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)


def sub(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element substraction
    """
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)


def mul(v0, k):
    """
        Input: 2 size 3 vectors
        Output: Size 3 vector with the per element multiplication
    """
    return V3(v0.x * k, v0.y * k, v0.z * k)


def dot(v0, v1):
    """
        Input: 2 size 3 vectors
        Output: Scalar with the dot product
    """
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def length(v0):
    """
        Input: 1 size 3 vector
        Output: Scalar with the length of the vector
    """
    return (v0.x ** 2 + v0.y ** 2 + v0.z ** 2) ** 0.5


def norm(v0):
    """
        Input: 1 size 3 vector
        Output: Size 3 vector with the normal of the vector
    """
    v0length = length(v0)

    if not v0length:
        return V3(0, 0, 0)

    return V3(v0.x / v0length, v0.y / v0length, v0.z / v0length)


def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]

    xs.sort()
    ys.sort()

    xmin = xs[0]
    xmax = xs[-1]
    ymin = ys[0]
    ymax = ys[-1]

    return xmin, xmax, ymin, ymax


def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x,
    )


def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y),
    )

    if abs(cz) < 1:
        return -1, -1, -1

    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz

    return w, v, u

def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)

def normalizeColorArray(colors_array):
    return [round(i*255) for i in colors_array]

def color(r,g,b):
	return bytes([b, g, r])

#Por motivos practicos seteo el color para mi fondo siempre.
Dark = color(0,0,0)

class Render(object):
    def __init__(self):
        self.framebuffer = []
        self.width = 1200
        self.height = 1200
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 1200
        self.viewport_height = 1200
        self.glClear()

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glViewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glClear(self):
        self.framebuffer = [
            [Dark for x in range(self.width)] for y in range(self.height)
        ]

    def glClearColor(self, r=1, g=1, b=1):
        # Solo acepta valores en 1
        normalized = normalizeColorArray([r,g,b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glVertex(self, x, y):
        final_x = round((x+1) * (self.viewport_width/2) + self.viewport_x)
        final_y = round((y+1) * (self.viewport_height/2) + self.viewport_y)
        self.point(final_x, final_y)

    def glColor(self, r=0, g=0, b=0):
        normalized = normalizeColorArray([r,g,b])
        self.color = color(normalized[0], normalized[1], normalized[2])

    def glCoordinate(self, value, is_vertical):
        real_coordinate = ((value+1) * (self.viewport_height/2) + self.viewport_y) if is_vertical else ((value+1) * (self.viewport_width/2) + self.viewport_x)
        return round(real_coordinate)

    def glLine(self, x0, y0, x1, y1) :
#Referencia de la calse de dennis y su repositorio
        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        y = y0
        threshold =  dx

        for x in range(x0, x1):
            self.point(y, x) if steep else self.point(x, y)
            
            offset += 2*dy

            if offset >= threshold:
                y += -1 if y0 > y1 else 1
                threshold += 2*dx
#Clase trabajada en clase
    def load(self, filename='default.obj', translate=[0,0], scale=[1,1]):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                vi1 = face[j][0] - 1
                vi2 = face[(j + 1) % vcount][0] - 1

                v1 = model.vertices[vi1]
                v2 = model.vertices[vi2]

                x1 = round((v1[0] * scale[0]) + translate[0])
                y1 = round((v1[1] * scale[1]) + translate[1])
                x2 = round((v2[0] * scale[0]) + translate[0])
                y2 = round((v2[1] * scale[1]) + translate[1])

                self.glLine(x1, y1, x2, y2)


    def glFinish(self, filename='output.bmp'):
        # starts creating a new bmp file
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Finishing placing points
        try:
            for x in range(self.height):
                for y in range(self.width):
                    f.write(self.framebuffer[x][y])
        except:
            print('Tu OBJ es demasiado grande, porfavor escalalo o comprueba sus componentes de tamaño')

        f.close()