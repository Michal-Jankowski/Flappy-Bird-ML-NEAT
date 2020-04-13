import neat
import pickle
from modules.GameAppManager import GameAppManager


def print_info(game):
    generations_info = game.crash_info
    for row, _ in generations_info:
        print(row['score'])


def play_game(best_generation, pickle_in):
    game = GameAppManager([best_generation], pickle_in)
    game.play()
    print_info(game)


def main():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        '../NEAT/config/feedforward-config'
    )
    pickle_in = open("best.pickle", "rb")
    best_generation = pickle.load(pickle_in)
    pickle_in.close()
    play_game(best_generation, config)


if __name__ == "__main__":
    main()
