#Graficas Sr4
#Jessica Ortiz
#20192

import struct

from obj import Obj

from vector import *


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)


def color(r, g, b):
    return bytes([b, g, r])


#Constructor
class Render(object):

    def __init__(self):
        self.viewPortX = 0
        self.viewPortY = 0
        self.height = 0
        self.width = 0
        self.clear_color = color(0, 0, 0)
        self.current_color = color(255, 255, 255)
        #Blanco y negro
        self.framebuffer = []
        
        self.glViewport(0,0,self.width, self.height)
        self.glClear() 

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

    #Mapa de bits de un solo color, en 3 dimensiones
    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zBuffer = [
            [-9999 for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zClear = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def glClearColor(self, r, g, b):
        self.clearColor = color(r * 255, b*255, g*255)
        self.glClear()

    #Da el color al punto creado en pantalla 
    def glPoint(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.framebuffer[x][y] = self.current_color


    #bounding box
    def bbox(self, A, B, C):
        coordenadas = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

        xmax, ymax = -10000, -10000
        xmin, ymin = 10000, 10000

        #definimos un tamaño para el bounding box y si nuestra iagen se pasa re asigne los valores
        for (x, y) in coordenadas:
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
            if x < xmin:
                xmin = x            
            if y < ymin:
                ymin = y
            

        return V3(xmin, ymin), V3(xmax, ymax)

    def cross(self, v1, v2):
        return (
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )

    def barycentric(self, A, B, C, P):
        cx, cy, cz = self.cross(
            V3(B.x - A.x, C.x - A.x, A.x - P.x),
            V3(B.y - A.y, C.y - A.y, A.y - P.y),
        )

        if abs(cz) < 1:
            return -1, -1, -1

        u = cx/cz
        v = cy/cz
        w = 1 - (cx + cy) / cz

        return w, v, u


    def triangle(self, A, B, C):

        N = (C - A) * (B - A)
        L = V3(0, 0, -1)
        i = N.normalize() @ L.normalize() # @ :matrix multiplication

        if i <= 0 or i > 1:
            return

        grey = round(255 * i)

        self.current_color = color(grey, grey, grey)

        Bmin, Bmax = self.bbox(A, B, C)
        for x in range(round(Bmin.x), round(Bmax.x) + 1):
            for y in range(round(Bmin.y), round(Bmax.y) + 1):
                w, v, u = self.barycentric(A, B, C, V3(x, y))

                if (w < 0 or v < 0 or u < 0):
                    continue

                z = A.z * w + B.z * v + C.z * u

                factor = round(z/self.width)

                if (self.zBuffer[x][y] < z):
                    self.zBuffer[x][y] = z
                    self.zClear[x][y] = color(factor, factor, factor)
                    self.glPoint(x, y)
        pass


    def transform(self, vertex, translate, scale):
        return V3(
            ((vertex[0] * scale[0]) + translate[0]),
            ((vertex[1] * scale[1]) + translate[1]),
            ((vertex[2] * scale[2]) + translate[2])
        )

    #Lee y renderiza archivos .obj 
    def glObjModel(self, file_name, translate, scale):
        model = Obj(file_name)

        for face in model.faces:
            if len(face) == 3:

                v1 = self.transform(model.vertices[face[0][0] - 1], translate, scale)
                v2 = self.transform(model.vertices[face[1][0] - 1], translate, scale)
                v3 = self.transform(model.vertices[face[2][0] - 1], translate, scale)

                self.triangle(v1, v2, v3)
            if len(face) == 4:

                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                vertices = [
                    self.transform(model.vertices[f1], translate, scale),
                    self.transform(model.vertices[f2], translate, scale),
                    self.transform(model.vertices[f3], translate, scale),
                    self.transform(model.vertices[f4], translate, scale)
                ]

                A, B, C, D = vertices

                self.triangle(A, B, C)
                self.triangle(A, C, D)

    # Función para crear la imagen
    def glFinish(self, filename):
        with open(filename, 'bw') as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))

            # file size
            file.write(dword(14 + 40 + self.height * self.width * 3))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[x][y])
            file.close()
