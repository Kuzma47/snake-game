import time
import pygame
from objects import Vector


class Controller:
    def __init__(self, game_engine):
        self.is_secret_activated = False
        self.all_keys = ''
        self.game_engine = game_engine
        self.dictionary_direction_by_key = {
            pygame.K_w: Vector.down(), pygame.K_s: Vector.up(),
            pygame.K_d: Vector.right(), pygame.K_a: Vector.left(),
            pygame.K_UP: Vector.down(), pygame.K_DOWN: Vector.up(),
            pygame.K_RIGHT: Vector.right(), pygame.K_LEFT: Vector.left()}
        self.pressed_keys = set()
        self.last_eat = time.time()

    def handle_key(self):
        for key in self.pressed_keys:
            if key in self.dictionary_direction_by_key:
                self.game_engine.snake.change_dir(
                    self.dictionary_direction_by_key[key])
            elif key == pygame.K_e and time.time() - self.last_eat > 0.1:
                self.last_eat = time.time()
                self.game_engine.spawn_food()

    def handle_keydown(self, key):
        ESCAPE = 27
        if key == ESCAPE:
            self.game_engine.snake.pause_game()
        self.all_keys += f'{key} '
        self.pressed_keys.add(key)
        self.check_keys()

    def handle_keyup(self, key):
        self.pressed_keys.remove(key)

    def check_keys(self):
        if '119 119 119 97 115 100 ' in self.all_keys:
            # [UP, UP, UP, LEFT, DOWN, RIGHT]
            self.is_secret_activated = True
            self.all_keys = ''
