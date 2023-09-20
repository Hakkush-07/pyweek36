from game import Planet, App

planets = [Planet(5, 0, 0.5, 0.5)]
planets = [Planet(5, 2, 0.5, 0.1), Planet(3, 4, 0.5, 0.2), Planet(2, 7, 0.5, 0.15), Planet(0, 8, 0.5, 0.25)]

app = App(planets=planets) # Cube(5, 0, 0, 1), 
app.run()

# , Planet(5, 2, 0.5, 0.5), Planet(3, 4, 0.5, 0.5), Planet(2, 7, 0.5, 0.5), Planet(0, 8, 0.5, 0.5)