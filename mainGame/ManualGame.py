import neat
import pickle
from modules.GameAppManager import GameAppManager

statistic_report = neat.StatisticsReporter()


def print_info(game):
    generations_info = game.crash_info
    for row, _ in generations_info:
        print("Score: " + str(row['score']))


def play_game(best_generation, pickle_in):
    game = GameAppManager([best_generation], pickle_in, 1)
    generation_number = best_generation.generation
    game.play(generation_number)
    print_info(game)


def main():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        '../NEAT/config/feedforward-config'
    )
    pickle_in = open("..//NEAT//pickle_file//best.pickle", "rb")
    best_generation = pickle.load(pickle_in)
    pickle_in.close()
    # set population of bird
    population = neat.population.Population(config)
    # enable output information of  neural network learning progress
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(statistic_report)

    play_game(best_generation, config)


if __name__ == "__main__":
    main()
