import pygame
from pygame.locals import *
import sys
from .colors import *
from .player import Player
from .camera import Camera

spaceship = pygame.image.load("spaceship.png")

"""
# draw edges
            for line in planet.edges:
                l = self.camera.render_line(line)
                if l:
                    clipped_l = l.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_l:
                        clipped_p1, clipped_p2 = clipped_l
                        pygame.draw.line(self.window, BLACK, self.to_window_tuple(clipped_p1), self.to_window_tuple(clipped_p2), 5)
            # draw corners
            for point in planet.corners:
                p = self.camera.render_point(point)
                if p:
                    clipped_p = p.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_p:
                        pygame.draw.circle(self.window, BLACK, self.to_window_tuple(clipped_p), 3)
"""


"""
for star in self.stars:
            p = self.camera.render_point(star.p)
            dx, dy, dz = self.camera.relative_position(star.p)
            distance = (dx * dx + dy * dy + dz * dz) ** 0.5
            print(dx, dy, dz, distance)
            # print(star.s(distance))
            if p:
                clipped_p = p.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                if clipped_p:
                    pygame.draw.circle(self.window, STAR, self.to_window_tuple(clipped_p), star.s(distance))
"""

class App:
    FPS = 120

    def __init__(self, planets=None):
        pygame.init()
        info = pygame.display.Info()
        self.w = info.current_w
        self.h = info.current_h
        self.window = pygame.display.set_mode((self.w, self.h), FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.player = Player()
        self.planets = planets if planets else []
        self.timer = 0
    
    def to_window_tuple(self, window_point):
        """
        converts WindowPoint to pygame window pixel coordinates
        """
        return window_point.x * self.w + 0.5 * self.w, -window_point.y * self.w + 0.5 * self.h
    
    def handle_quit(self):
        """
        handles quit events, esc key and exit button
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def draw_things(self):
        """
        draws objects on the window
        """
        self.window.fill(SPACE)
        polygons = []
        for planet in self.planets:
            # draw faces
            for polygon in planet.faces:
                f = self.camera.render_polygon(polygon)
                dx, dy, dz = self.camera.relative_position(polygon.center)
                distance = (dx * dx + dy * dy + dz * dz) ** 0.5
                if f:
                    clipped_f = f.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_f:
                        polygons.append((distance, [self.to_window_tuple(p) for p in clipped_f.vertices]))
                        # pygame.draw.polygon(self.window, YELLOW, [self.to_window_tuple(p) for p in clipped_f.vertices])
            planet.update()
        for distance, vertices in sorted(polygons, key=lambda x: -x[0]):
            u = int(255 - 15 * distance)
            color = (u, u, 100)
            pygame.draw.polygon(self.window, color, vertices)
        self.window.blit(pygame.font.Font(None, 32).render(str(int(App.FPS)), True, WHITE), (10, 10))
        self.window.blit(pygame.transform.scale(spaceship.convert_alpha(), (self.w, int(self.w * spaceship.get_height()/ spaceship.get_width()))), (0, 0))
        pygame.display.flip()

    def handle_movement(self, dt):
        """
        handles movement based on WASD key presses
        """
        keys = pygame.key.get_pressed()
        a = keys[K_a] - keys[K_d]
        b = keys[K_w] - keys[K_s]
        c = keys[K_x] - keys[K_z] # (keys[K_LCTRL] or keys[K_RCTRL]) - (keys[K_LSHIFT] or keys[K_RSHIFT])
        self.camera.position += self.player.move(a, b, c, dt, self.camera.rotation.a)
    
    def handle_rotation(self, dt):
        """
        handles rotation based on mouse movements
        """
        a, b = pygame.mouse.get_rel()
        self.camera.rotation += self.player.rotate(a, b, dt)
    
    def time_calculations(self):
        fps = self.clock.get_fps()
        dt = self.clock.tick() * 0.001
        self.timer += dt
        # update fps every second
        if self.timer > 1:
            self.timer = 0
            App.FPS = fps if fps else 120
        return dt

    def run(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        while True:
            dt = self.time_calculations()
            self.handle_quit()
            self.draw_things()
            self.handle_movement(dt)
            self.handle_rotation(dt)
            
