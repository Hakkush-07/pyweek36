from .world import WorldPoint, WorldLine, WorldPolygon

phi = (1 + 5**0.5) / 2
corners = [(0.0, i, j) for i in [-1.0, 1.0] for j in [-phi, phi]] + [(i, j, 0.0) for i in [-1.0, 1.0] for j in [-phi, phi]] + [(j, 0.0, i) for i in [-1.0, 1.0] for j in [-phi, phi]]
edges = [(0, 2), (1, 3), (4, 6), (5, 7), (8, 10), (9, 11), (0, 4), (0, 6), (0, 8), (0, 9), (2, 8), (2, 5), (2, 7), (2, 9), (1, 4), (1, 6), (1, 10), (1, 11), (3, 5), (3, 7), (3, 10), (3, 11), (4, 8), (4, 10), (5, 8), (5, 10), (6, 9), (6, 11), (7, 9), (7, 11)]
faces = [(0, 2, 8), (0, 2, 9), (0, 4, 6), (0, 4, 8), (0, 6, 9), (1, 3, 10), (1, 3, 11), (1, 4, 6), (1, 4, 10), (1, 6, 11), (2, 5, 8), (2, 7, 5), (2, 7, 9), (3, 5, 7), (3, 5, 10), (3, 7, 11), (4, 8, 10), (5, 8, 10), (6, 9, 11), (7, 9, 11)]

class Icosahedron:
    """
    planet in the world
    center coordinates are WorldPoint
    s is scale
    """
    def __init__(self, cx, cy, cz, s):
        self.x = cx
        self.y = cy
        self.z = cz
        self.center = WorldPoint(self.x, self.y, self.z)
        self.s = s
        self.k = 0.0

        self.corners = [WorldPoint(self.x + x * s, self.y + y * s, self.z + z * s) for x, y, z in corners]
        self.edges = [WorldLine(self.corners[i], self.corners[j]) for i, j in edges]
        self.faces = [WorldPolygon([self.corners[i], self.corners[j], self.corners[k]]) for i, j, k in faces]
    
    def update_polyhedron(self, new_corners):
        self.corners = new_corners
        self.edges = [WorldLine(self.corners[i], self.corners[j]) for i, j in edges]
        self.faces = [WorldPolygon([self.corners[i], self.corners[j], self.corners[k]]) for i, j, k in faces]

class Planet(Icosahedron):
    def __init__(self, cx, cy, cz, s):
        super().__init__(cx, cy, cz, s)
    
    def update(self):
        self.k += 0.01
        new = [self.center + WorldPoint(*c).rotate_z(self.k).rotate_y(self.k).rotate_x(self.k) * self.s for c in corners]
        self.update_polyhedron(new)
