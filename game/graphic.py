import pygame
from objects import MapCell


class View:
    def __init__(self, game_engine):
        self.width, self.height = game_engine.map_size
        self.scale = 25
        self.surf = self.create_window(game_engine.map_size)
        self.game_engine = game_engine
        self.game_engine.view = self
        self.color = {MapCell.empty: pygame.Color("#57A14F"),
                      MapCell.snake_tail: pygame.Color("#2F7028"),
                      MapCell.snake_pre_tail: pygame.Color("#17680E"),
                      MapCell.snake_body: pygame.Color("#106806"),
                      MapCell.snake_head: pygame.Color("#076600"),
                      MapCell.common_food: pygame.Color("#FF0000"),
                      MapCell.wall: pygame.Color("#3C3C3C"),
                      MapCell.speed_food: pygame.Color("#0011FF"),
                      MapCell.slowness_food: pygame.Color("#4F62A1"),
                      MapCell.score_food: pygame.Color("#FFF603"),
                      MapCell.decrease_food: pygame.Color("#724925")}
        pygame.display.set_caption("Snake")

    def update(self):
        for w in range(self.width):
            for h in range(self.height):
                cell = self.game_engine.map[h][w]
                self.fill_pixel_with_color(self.color[cell], [h, w])
        for seg in self.game_engine.snake.get_segments():
            self.fill_pixel_with_color(self.color[seg.type],
                                       [seg.pos.y, seg.pos.x])
        self.draw_text(self.game_engine.snake)
        pygame.display.update()

    def create_window(self, size):
        border_color = [200] * 3
        surface = pygame.display.set_mode(
            [size[0] * self.scale,
             size[1] * self.scale])
        for i in range(0, size[0]):
            pygame.draw.line(surface, border_color,
                             [i * self.scale, 0],
                             [i * self.scale, size[1] * self.scale])
        for i in range(0, size[1]):
            pygame.draw.line(surface, border_color,
                             [0, i * self.scale],
                             [size[0] * self.scale, i * self.scale])
        return surface

    def fill_with_color(self, screen_color):
        self.surf.fill(screen_color)
        w, h = self.surf.get_size()
        for i in range(0, w):
            pygame.draw.line(self.surf, [200] * 3,
                             [i * self.scale, 0],
                             [i * self.scale, h * self.scale])
        for i in range(0, h):
            pygame.draw.line(self.surf, [200] * 3,
                             [0, i * self.scale],
                             [w * self.scale, i * self.scale])

    def fill_pixel_with_color(self, color, pos):
        pygame.draw.rect(self.surf,
                         color,
                         [pos[1] * self.scale,
                          pos[0] * self.scale,
                          self.scale, self.scale]
                         )

    def draw_text(self, snake):
        font = pygame.font.Font(None, 50)
        score = font.render(f'Score: {snake.score}/{snake.win_score}',
                            True, pygame.Color("#000000"))
        lives = font.render(f'Lives: {snake.health}/3',
                            True, pygame.Color("#000000"))
        score.set_alpha(127)
        lives.set_alpha(127)
        self.surf.blit(score, [0, 0])
        self.surf.blit(lives, [0, 40])
