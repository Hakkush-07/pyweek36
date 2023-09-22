from .world import WorldPoint
from random import random

max_gravity = 0.0

def randomx():
    return random() - 0.5

def clip(x, mn=0):
    return mn if x < mn else 1 if x > 1 else x

class Gravity:
    def __init__(self) -> None:
        self.r1 = WorldPoint(randomx(), randomx(), randomx())
        self.r2 = WorldPoint(randomx(), randomx(), randomx())
        self.r3 = WorldPoint(randomx(), randomx(), randomx())
        self.a = random() / 2 + 0.5
    
    def get(self, position):
        r1x, r1y, r1z = self.r1.normalize()
        r2x, r2y, r2z = self.r2.normalize()
        r3x, r3y, r3z = self.r3.normalize()
        px, py, pz = position.normalize()
        fx = r1x * px + r1y * py + r1z * pz
        fy = r2x * px + r2y * py + r2z * pz
        fz = r3x * px + r3y * py + r3z * pz
        return WorldPoint(fx, fy, fz).normalize() * self.a * max_gravity

    def update(self, dt):
        dr1 = WorldPoint(randomx(), randomx(), randomx()) * 0.1 * dt
        self.r1 += dr1
        self.r1.x = clip(self.r1.x)
        self.r1.y = clip(self.r1.y)
        self.r1.x = clip(self.r1.z)

        dr2 = WorldPoint(randomx(), randomx(), randomx()) * 0.1 * dt
        self.r2 += dr2
        self.r2.x = clip(self.r2.x)
        self.r2.y = clip(self.r2.y)
        self.r2.x = clip(self.r2.z)

        dr3 = WorldPoint(randomx(), randomx(), randomx()) * 0.1 * dt
        self.r3 += dr3
        self.r3.x = clip(self.r3.x)
        self.r3.y = clip(self.r3.y)
        self.r3.x = clip(self.r3.z)

        da = randomx()
        self.a += da * dt * 5
        self.a = clip(self.a, 0.5)
        
    
