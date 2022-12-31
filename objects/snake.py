from .vector import Vector
from .map_item import MapCell
import pygame
from random import randint


class SnakeSegment:
    def __init__(self, pos, segment, direction, next_segment=None):
        self.dir = direction
        self.pos = pos
        self.type = segment
        self.next = next_segment


class Snake:
    def __init__(self, game_engine, win_score):
        self.invisibility = 3
        self.win_score = win_score
        self.game_engine = game_engine
        self.map = game_engine.map
        start_position = Vector(len(self.map[0]) // 2, len(self.map) // 2)
        self.head = self.tail = None
        self.new_head_dir = Vector.zero()
        self.health = 3
        self.score = 0
        self.move_delays = [80, 150, 200, 250, 350]
        self.move_delay_index = 2
        self.paused = False
        self.is_segments_updated = True
        self.segments = None
        self.head = SnakeSegment(
            start_position,
            MapCell.snake_head,
            Vector.zero()
        )
        pre_tail = SnakeSegment(
            start_position,
            MapCell.snake_pre_tail,
            Vector.zero(),
            self.head
        )
        self.tail = SnakeSegment(
            start_position,
            MapCell.snake_tail,
            Vector.zero(),
            pre_tail
        )

    @staticmethod
    def play_sound(sound):
        sound2 = pygame.mixer.Sound(sound)
        sound2.play()

    def stop_game(self, code):
        self.game_engine.stop_flag = True
        self.game_engine.exit_code = code

    def pause_game(self):
        self.paused = not self.paused
        if self.paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def handle_score(self):
        if self.score >= self.win_score:
            self.stop_game(2)

    def move_tail(self, new_tail):
        self.tail = new_tail
        self.tail.type = MapCell.snake_tail
        if self.tail.next is not None \
                and self.tail.next.type != MapCell.snake_head:
            self.tail.next.type = MapCell.snake_pre_tail

    def move_head(self, new_head):
        self.head.type = MapCell.snake_body
        self.head.next = new_head
        self.head = new_head

    def on_collision(self, pos):
        map_obj = self.map[pos.y][pos.x]
        if map_obj not in (MapCell.empty, MapCell.wall):
            if map_obj == MapCell.score_food:
                self.score += 4
            if map_obj == MapCell.speed_food:
                self.move_delay_index = max(self.move_delay_index - 1, 0)
            if map_obj == MapCell.slowness_food:
                self.move_delay_index = min(
                    self.move_delay_index + 1, len(self.move_delays))

            self.eat(map_obj == MapCell.decrease_food)
            self.handle_score()

        elif map_obj == MapCell.wall and self.invisibility < 0:
            self.play_sound('wall.mp3')
            self.invisibility = 3
            self.health -= 1
            self.score = max(self.score - 10, 0)
            if self.health < 1:
                self.stop_game(1)

        if map_obj == MapCell.wall and self.invisibility < 0\
                or map_obj != MapCell.wall:
            self.map[pos.y][pos.x] = MapCell.empty

        snake_segment = self.get_segment_by_pos(pos)
        if snake_segment is not None and \
                snake_segment.type in \
                [MapCell.snake_body, MapCell.snake_pre_tail]:
            self.move_tail(snake_segment)

    def move(self):
        if self.paused:
            return
        self.head.dir = self.new_head_dir
        if self.head.dir == Vector.zero():
            return
        self.invisibility -= 1
        nxt_p = self.head.pos + self.head.dir
        if nxt_p.x < 0 or nxt_p.x >= self.game_engine.map_size[0]\
                or nxt_p.y < 0 or nxt_p.y >= self.game_engine.map_size[1]:
            nxt_p = Vector((nxt_p.x + self.game_engine.map_size[0])
                           % self.game_engine.map_size[0],
                           (nxt_p.y + self.game_engine.map_size[1])
                           % self.game_engine.map_size[1])

        self.on_collision(nxt_p)
        self.move_tail(self.tail.next)

        self.move_head(
            SnakeSegment(nxt_p, MapCell.snake_head, self.head.dir))
        pos = [segment.pos for segment in self.segments]
        if pos.count(self.head.pos) == 1 and len(self.segments) > 4:
            self.play_sound('wall.mp3')
            self.health -= 3
            self.stop_game(1)
        self.is_segments_updated = True

    def eat(self, is_decreasing=False):
        self.play_sound('eat.wav')
        if is_decreasing:
            if len(self.segments) > 3:
                self.tail = self.segments[1]
        else:
            self.tail = SnakeSegment(
                self.tail.pos,
                MapCell.snake_tail,
                self.tail.dir,
                self.tail)
        self.score += 1
        self.game_engine.spawn_food()

    def get_segment_by_pos(self, pos):
        for s in self.get_segments():
            if s.pos == pos:
                return s
        return None

    def get_segments(self):
        if not self.is_segments_updated:
            return self.segments
        segments_pos = []
        cur_segment = self.tail
        while cur_segment is not None:
            segments_pos.append(cur_segment)
            cur_segment = cur_segment.next
        self.is_segments_updated = False
        self.segments = segments_pos
        return segments_pos

    def change_dir(self, new_dir):
        if self.head.dir != -new_dir and self.head.dir != new_dir:
            self.new_head_dir = new_dir

    def activate_secret(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == MapCell.wall:
                    self.map[i][j] = MapCell.empty
                if randint(0, 10) < 2:
                    self.map[i][j] = self.game_engine.get_random_item()
