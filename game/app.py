import pygame
from pygame.locals import *
import sys
from .colors import *
from .player import Player
from .camera import Camera
from .gravity import Gravity
from .icosahedron import Planet

spaceship = pygame.image.load("spaceship.png")

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
        self.gravity = Gravity()
        self.planets = planets if planets else []
        self.timer = 0
        self.free = False
        self.start_screen = True
        self.start_planet = Planet(4, 0, 0, 0.5, 0.001, 180)
        self.start_center = self.to_window_tuple(self.camera.render_point(self.start_planet.center))
        self.start_mouse_inside = False

        self.G = 0, 0, 0
        self.V = 0, 0, 0
        
    def to_window_tuple(self, window_point):
        """
        converts WindowPoint to pygame window pixel coordinates
        """
        return window_point.x * self.w + 0.5 * self.w, -window_point.y * self.w + 0.5 * self.h
    
    def handle_quit_and_free(self):
        """
        handles quit events, esc key and exit button
        if u is pressed, switches between free mode and game mode
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_u:
                    if not self.start_screen:
                        if self.free:
                            self.free = False
                        else:
                            self.free = True
                            self.player.reset_v()
            elif event.type == MOUSEBUTTONDOWN:
                if self.start_screen and self.start_mouse_inside:
                    self.start_screen = False
                    self.hide_mouse()
    
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
                if f:
                    clipped_f = f.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_f:
                        distance = abs(self.camera.relative_position(polygon.center))
                        normal = polygon.normal(planet.center)
                        polygons.append((distance, [self.to_window_tuple(p) for p in clipped_f.vertices], normal, planet.color))
                        # pygame.draw.polygon(self.window, YELLOW, [self.to_window_tuple(p) for p in clipped_f.vertices])
            planet.update()
        for distance, vertices, normal, hue in sorted(polygons, key=lambda x: -x[0]):
            light = self.camera.light(normal)
            color = hsv2rgb(hue, 1.0, light)
            pygame.draw.polygon(self.window, color, vertices)
        self.window.blit(pygame.transform.scale(spaceship.convert_alpha(), (self.w, int(self.w * spaceship.get_height()/ spaceship.get_width()))), (0, 0))
        self.window.blit(pygame.font.Font(None, 32).render(str(int(App.FPS)), True, WHITE), (10, 10))
        self.window.blit(pygame.font.Font(None, 32).render("G: " + str(self.G), True, WHITE), (10, 110))
        self.window.blit(pygame.font.Font(None, 32).render("V: " + str(self.V), True, WHITE), (10, 210))
        pygame.display.flip()
    
    def draw_start_screen(self):
        self.window.fill(SPACE)
        polygons = []
        for polygon in self.start_planet.faces:
            f = self.camera.render_polygon(polygon)
            if f:
                clipped_f = f.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                if clipped_f:
                    distance = abs(self.camera.relative_position(polygon.center))
                    normal = polygon.normal(self.start_planet.center)
                    polygons.append((distance, [self.to_window_tuple(p) for p in clipped_f.vertices], normal, self.start_planet.color))
        self.start_planet.update()
        for distance, vertices, normal, hue in sorted(polygons, key=lambda x: -x[0]):
            light = self.camera.light(normal)
            color = hsv2rgb(hue, 1.0, light)
            pygame.draw.polygon(self.window, color, vertices)
        cx, cy = self.start_center
        k = 100
        mx, my = pygame.mouse.get_pos()
        if abs(mx - cx) < k and abs(my - cy) < k:
            font = 100
            self.start_planet.r = 0.003
            self.start_mouse_inside = True
        else:
            font = 64
            self.start_planet.r = 0.001
            self.start_mouse_inside = False
        x = pygame.font.Font(None, font).render("START", True, WHITE)
        w = x.get_bounding_rect().width
        h = x.get_bounding_rect().height
        
        self.window.blit(x, (cx - w // 2, cy - h // 2))
        pygame.display.flip()

    def handle_movement(self, dt):
        """
        handles movement based on WASD key presses
        """
        keys = pygame.key.get_pressed()
        a = keys[K_a] - keys[K_d]
        b = keys[K_w] - keys[K_s]
        c = keys[K_t] - keys[K_g] # (keys[K_LCTRL] or keys[K_RCTRL]) - (keys[K_LSHIFT] or keys[K_RSHIFT])
        self.camera.position += self.player.move(a, b, c, dt, self.camera.rotation.a)
    
    def handle_movement2(self, dt):
        """
        applies force based on WASD key presses
        """
        keys = pygame.key.get_pressed()
        a = keys[K_a] - keys[K_d]
        b = keys[K_w] - keys[K_s]
        c = keys[K_t] - keys[K_g]
        self.player.accelerate(a, b, c, dt, self.camera.rotation.a)
    
    def handle_rotation(self, dt):
        """
        handles rotation based on mouse movements
        """
        a, b = pygame.mouse.get_rel()
        self.camera.rotation += self.player.rotate(a, b, dt)
    
    def handle_rotation2(self, dt):
        """
        handles rotation based on keys
        """
        keys = pygame.key.get_pressed()
        r = keys[K_m] - keys[K_n]
        self.camera.rotation += self.player.rotate(r, 0, dt)
    
    def time_calculations(self):
        fps = self.clock.get_fps()
        dt = self.clock.tick() * 0.001
        self.timer += dt
        # update fps every second
        if self.timer > 1:
            self.timer = 0
            App.FPS = fps if fps else 120
        return dt
    
    def hide_mouse(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    
    def run(self):
        while True:
            if self.start_screen:
                self.handle_quit_and_free()
                self.draw_start_screen()
            else:
                dt = self.time_calculations()
                self.handle_quit_and_free()
                self.draw_things()
                if self.free:
                    self.handle_movement(dt)
                    self.handle_rotation(dt)
                else:
                    self.handle_movement2(dt)
                    self.handle_rotation2(dt)
                    self.gravity.update(dt)
                    g = self.gravity.get(self.camera.position)
                    # self.G = round(abs(g), 2)
                    gx, gy, gz = g
                    self.G = (round(gx, 2), round(gy, 2), round(gz, 2))
                    acc = g * dt
                    self.player.v += acc
                    vx, vy, vz = self.player.v
                    # self.V = round(abs(self.player.v), 2)
                    self.V = (round(vx, 2), round(vy, 2), round(vz, 2))
                if dt:
                    self.camera.position += self.player.v * dt
                
