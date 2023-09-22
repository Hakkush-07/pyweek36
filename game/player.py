from math import sqrt, sin, cos
from .world import WorldPoint
from .rotation import Rotation

class Player:
    def __init__(self):
        self.velocity = 4.0
        self.sensitivity = 2.0
        self.force = 2.0
        self.v = WorldPoint(0, 0, 0)

    def rotate(self, horizontal, vertical, dt):
        """
        horizontal is horizontal mouse movement
        vertical is vertical mouse movement
        dt is delta time
        returns delta rotation
        """
        return Rotation(-horizontal * self.sensitivity * dt, -vertical * self.sensitivity * dt)

    def move(self, lr, ud, cs, dt, rotation_xy):
        """
        lr is -1, 0, 1 for right, no movement, left
        ud is -1, 0, 1 for forward, no movement, backward
        cs is -1, 0, 1 for down, no movement, up
        dt is delta time
        rotation_xy is the xy plane rotation of the camera
        returns delta movement
        """
        if lr == 0 and ud == 0 and cs == 0:
            # no movement
            return WorldPoint(0, 0, 0)
        
        distance = self.velocity * dt / sqrt(lr ** 2 + ud ** 2 + cs ** 2)
        s, c = sin(rotation_xy), cos(rotation_xy)
        dx = (c * ud - s * lr) * distance
        dy = (s * ud + c * lr) * distance
        dz = cs * distance
        return WorldPoint(dx, dy, dz)
    
    def accelerate(self, lr, ud, cs, dt, rotation_xy):
        """
        lr is -1, 0, 1 for right, no movement, left
        ud is -1, 0, 1 for forward, no movement, backward
        cs is -1, 0, 1 for down, no movement, up
        dt is delta time
        rotation_xy is the xy plane rotation of the camera
        updates player 3d velocity
        """
        if lr == 0 and ud == 0 and cs == 0:
            # no force
            return
        
        u = dt / sqrt(lr ** 2 + ud ** 2 + cs ** 2)
        s, c = sin(rotation_xy), cos(rotation_xy)
        dvx = (c * ud - s * lr) * u
        dvy = (s * ud + c * lr) * u
        dvz = cs * u
        dv = WorldPoint(dvx, dvy, dvz) * self.force
        self.v += dv
        
    def reset_v(self):
        self.v = WorldPoint(0, 0, 0)
