import pygame
from pygame.locals import *
import sys
from .colors import *

class App:
    FPS = 120

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.w = info.current_w
        self.h = info.current_h
        self.window = pygame.display.set_mode((self.w, self.h), FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.timer = 0.0
    
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
        self.window.fill(LIGHT_BLUE)
        self.window.blit(pygame.font.Font(None, 32).render(str(int(App.FPS)), True, BLACK), (10, 10))
        pygame.display.update()

    def handle_movement(self, dt):
        """
        handles movement based on WASD key presses
        """
        keys = pygame.key.get_pressed()
        a = keys[K_a] - keys[K_d]
        b = keys[K_w] - keys[K_s]
    
    def handle_rotation(self, dt):
        """
        handles rotation based on mouse movements
        """
        a, b = pygame.mouse.get_rel()
    
    def handle_jump(self, dt):
        """
        handles jumping and space key presses
        """
        space = pygame.key.get_pressed()[K_SPACE]
    
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
            self.handle_jump(dt)
            