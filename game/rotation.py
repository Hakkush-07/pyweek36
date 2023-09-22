from math import pi

def clip_z_rotation(zr, epsilon):
    return -pi / 2 + epsilon if zr < -pi / 2 + epsilon else pi / 2 - epsilon if zr > pi / 2 - epsilon else zr

class Rotation:
    def __init__(self, alpha, beta):
        """
        rotation
        alpha: rotation in xy plane (0 means +x, pi/2 means +y while beta is 0)
        beta: rotation up and down (0 means ahead, pi/2 means up, -pi/2 means down)
        """
        self.alpha = self.a = alpha
        self.beta = self.b = beta
    
    def __repr__(self):
        return f"Rotation({self.a}, {self.b}))"
    
    def __add__(self, other):
        return Rotation(self.a + other.a, clip_z_rotation(self.b + other.b, 0.1))

    def __iadd__(self, other):
        return self + other
