import time
from game_objects.other.game import Game, GameState

if __name__ == "__main__":
    game : Game = Game()
    running : bool = True
    state : GameState = GameState.PLAY
    while running:
        state = game.run(state)
        match state:
            case GameState.PLAY: continue
            case GameState.QUIT: running = False
            case GameState.WIN:
                time.sleep(2)
                continue
