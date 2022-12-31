import enum


class MapCell(enum.Enum):
    empty = 0
    wall = 1
    snake_head = 2
    snake_body = 3
    snake_pre_tail = 4
    snake_tail = 5
    common_food = 6
    speed_food = 7
    slowness_food = 8
    score_food = 9
    decrease_food = 10


ITEM_BY_KEY = {
    ' ': MapCell.empty,
    '#': MapCell.wall,
    'O': MapCell.common_food,
    '-': MapCell.decrease_food,
    '$': MapCell.score_food,
    '>': MapCell.speed_food,
    '<': MapCell.slowness_food
}


def parse_map(level):
    game_map = [[MapCell.empty for _ in range(len(level[0]))]
                for _ in range(len(level))]
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            game_map[y][x] = ITEM_BY_KEY[level[y][x]]
    return game_map
