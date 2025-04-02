from game import Game, GameState

if __name__ == "__main__":
    game : Game = Game()
    running : bool = True
    while running:
        state : GameState = game.run()
        match state:
            case GameState.PLAY: continue
            case GameState.QUIT: running = False
            case GameState.WIN: continue
