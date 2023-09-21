from game import Planet, App, YELLOW
from random import choice

planet_rotations = [0.001, 0.002, 0.003, 0.004, 0.005]
planet_sizes = [5, 4, 3, 2, 1]
planet_count = 10

planets = []
for i in range(-planet_count, planet_count):
    planet = Planet(30 * (i % 10), 30 * (i // 10), 0, choice(planet_sizes), choice(planet_rotations), YELLOW)
    planets.append(planet)

app = App(planets=planets)
app.run()
