#Graficas Sr4
#Jessica Ortiz
#20192

#funciones de operaciones para vectores

class V3(object):
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return V3(
                self.x * other,
                self.y * other,
                self.z * other
            )
            
#producto cruz
#el resultado es un vector perpendicular a los dos vectores, solo funciona en vectores de 3 dimensiones
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __repr__(self):
        return "V3(%s,%s,%s)" % (self.x, self.y, self.z)


#longitud

    def len(self):
        return(self.x**2 + self.y**2 + self.z**2)**0.5

#producto punto nos da un numero escalar

#es util para dererminar la direccion relativa entre dos vectores
#si el producto punto es 1, ambos vectores tienen la misma direccion
#si es 0, ambos son perpendiculares
#si es -1, tienen direcciones opuestas.

    def __matmul__(self, other):
        return( self.x * other.x + self.y * other.y + self.z * other.z)

    #normalizar vector
    #si es 1 van en la misma direccion
    #si es 0.algo es 
    def normalize(self):
        return self * (1/self.len())


