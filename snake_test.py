import unittest

from game import Controller, GameEngine
from levels import LEVELS
from objects import MapCell, parse_map, Snake, Vector


class TestLevels(unittest.TestCase):
    def test_all_levels_are_minimum_5_by_5(self):
        for level in LEVELS:
            self.assertTrue(len(level[0]) > 4)

    def test_all_levels_are_square(self):
        for level in LEVELS:
            self.assertTrue(len(level[0]) == len(level[0][0]))

    def test_is_correct_win_score(self):
        for level in LEVELS:
            self.assertTrue(type(level[1]) is int and level[1] > 0)


class TestObjects(unittest.TestCase):
    def test_items_by_key(self):
        from objects.map_item import ITEM_BY_KEY
        self.assertTrue(ITEM_BY_KEY[' '] == MapCell.empty)
        self.assertTrue(ITEM_BY_KEY['#'] == MapCell.wall)

    def test_parse_map_correct(self):
        empty_level = [[' '] * 5] * 5
        level_with_wall = ['   ', ' # ', '   ']

        empty_map = parse_map(empty_level)
        map_with_wall = parse_map(level_with_wall)

        self.assertTrue(empty_map == [[MapCell.empty] * 5] * 5)
        self.assertTrue(
            map_with_wall[0] == map_with_wall[2] == [MapCell.empty] * 3,
            map_with_wall[1] == [MapCell.empty,
                                 MapCell.wall,
                                 MapCell.empty])

    def test_items_enum_correct(self):
        self.assertTrue(MapCell.empty.value == 0)
        self.assertTrue(MapCell.decrease_food.value == 10)

    def test_snake_win_score(self):
        level = ['   ', ' # ', '   ']
        game_engine = GameEngine(level)
        for win_score in range(-1, 10):
            snake = Snake(game_engine, win_score)
            self.assertTrue(snake.win_score == win_score)

    def test_vector(self):
        self.assertTrue(Vector.zero() == Vector(0, 0))
        self.assertTrue(-Vector.up() == Vector(0, -1))
        self.assertTrue(Vector(2, 1) - Vector(1, 2) == Vector(1, -1))


class TestGameModules(unittest.TestCase):
    def test_pause(self):
        level = [[' '] * 3] * 3
        game_engine = GameEngine(level)
        controller = Controller(game_engine)
        self.assertTrue(not controller.game_engine.snake.paused)

    def test_controller(self):
        level = [[' '] * 3] * 3
        game_engine = GameEngine(level)
        controller = Controller(game_engine)
        controller.handle_keydown(100)
        self.assertTrue(100 in controller.pressed_keys)
        controller.handle_keyup(100)
        self.assertTrue(100 not in controller.pressed_keys)

    def test_game_engine(self):
        level = [[' '] * 3] * 3
        game_engine = GameEngine(level)
        self.assertIsNotNone(game_engine)
        self.assertTrue(game_engine.map_size == [1, 3])
        food = []
        for _ in range(100):
            food.append(game_engine.get_random_item())
        self.assertTrue(MapCell.common_food in food)

    def test_view(self):
        level = [[' '] * 3] * 3
        game_engine = GameEngine(level)
        self.assertIsNotNone(game_engine)


if __name__ == '__main__':
    unittest.main()
