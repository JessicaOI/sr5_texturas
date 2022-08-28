#Graficas Sr4
#Jessica Ortiz
#20192

from cargar import Render

w = 1000
h = 1000
rend = Render()
rend.glCreateWindow(w, h)

rend.glViewport(int(0),
                int(0), 
                int(w/1), 
                int(h/1))

def glInit():
    return rend

if __name__ == '__main__':

    rend = glInit()

    #cargar .obj (posicion inicial), (escala)
    rend.glObjModel('FlowerPot.obj', (500, 10, 0), (200, 200, 200))
    
    rend.glFinish('out.bmp')