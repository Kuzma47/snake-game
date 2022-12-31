import threading
import pygame
from game import GameEngine, View, Controller
from levels import LEVELS


def handle(controller, game_engine):
    while not game_engine.stop_flag:
        if controller.is_secret_activated:
            controller.is_secret_activated = False
            game_engine.snake.activate_secret()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                controller.handle_keydown(event.key)
            elif event.type == pygame.KEYUP:
                controller.handle_keyup(event.key)
            elif event.type == pygame.QUIT:
                game_engine.stop_flag = True
                return 0
        controller.handle_key()
    return game_engine.exit_code


def start_game():
    current_level = 0
    while True:
        pygame.init()
        pygame.mixer.music.load('back.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=99999)
        game_engine = GameEngine(LEVELS[
                                     min(current_level, len(LEVELS) - 1)])
        View(game_engine)
        threading.Thread(target=game_engine.run).start()
        exit_code = handle(Controller(game_engine), game_engine)
        if exit_code == 0:
            print(f'You exit game.')
            break
        elif exit_code == 1:
            print(f'You die! Try one more time.')
        elif exit_code == 2:
            print(f'You completed level!')
            current_level += 1
        pygame.time.delay(300)
        pygame.quit()


if __name__ == '__main__':
    start_game()
