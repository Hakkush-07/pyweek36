from game import Planet, App, YELLOW, generate_random_planets
from random import choice, random

"""
planet_rotations = [0.001, 0.002, 0.003, 0.004, 0.005]
planet_sizes = [5, 4, 3, 2, 1]
planet_count = 10
planets = []
for i in range(-planet_count, planet_count):
    for level in range(5):
        if i == 0 and level == 0:
            continue
        planet = Planet(10 * (i % 10), 10 * (i // 10), 10 * level, choice(planet_sizes) / 3, choice(planet_rotations), random() * 360)
        planet2 = Planet(-10 * (i % 10), -10 * (i // 10), 10 * level, choice(planet_sizes) / 3, choice(planet_rotations), random() * 360)
        planets.append(planet)
        planets.append(planet2)
p = planets
"""

p = generate_random_planets((-200, 200), (-200, 200), (-100, 100), 10, 30)
print(len(p))

app = App(planets=p)
app.run()
