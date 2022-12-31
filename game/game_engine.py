import random
from objects import Snake, Vector, parse_map, MapCell
import pygame

KEY_BY_VECTOR = {
    Vector.zero(): '*',
    Vector.left(): '<',
    Vector.right(): '>',
    Vector.up(): '!',
    Vector.down(): '^'
}


class GameEngine:
    def __init__(self, level):
        self.exit_code = None
        self.map = parse_map(level[0])
        self.map_size = [len(self.map[0]), len(self.map)]
        self.snake = Snake(self, level[1])
        self.view = None
        self.stop_flag = False
        self.empty_cells = set()
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                if self.map[y][x] == MapCell.empty:
                    self.empty_cells.add(Vector(x, y))
        self.spawn_food(3)

    def update_map(self, updates):
        for upd in updates:
            x, y = upd[0].x, upd[0].y
            self.map[y][x] = upd[1]

    @staticmethod
    def get_random_item():
        items_with_chance = {
            MapCell.common_food: 8,
            MapCell.decrease_food: 2,
            MapCell.score_food: 2,
            MapCell.speed_food: 2,
            MapCell.slowness_food: 2
        }
        all_items = []
        for item, count in items_with_chance.items():
            all_items.extend(item for _ in range(count))
        return random.choice(all_items)

    def spawn_food(self, count=1):
        self.empty_cells.add(self.snake.head.pos)
        not_available_cells = set()
        for seg in self.snake.get_segments():
            not_available_cells.add(seg.pos)
        available_cells = self.empty_cells - not_available_cells
        for _ in range(count):
            if self.empty_cells:
                spawn_pos = random.choice(list(available_cells))
                self.map[spawn_pos.y][spawn_pos.x] = \
                    self.get_random_item()

    def run(self):
        while not self.stop_flag:
            pygame.time.delay(
                self.snake.move_delays[self.snake.move_delay_index])
            self.snake.move()
            self.view.update()
