import neat
import pickle
from modules.GameAppManager import GameAppManager


# mainGame method of train file
# configuration of NEAT algorithm from file
def main():
    global statistic_report
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        '../NEAT/config/feedforward-config'
    )
    statistic_report = neat.StatisticsReporter()
    # set population of bird
    population = neat.population.Population(config)
    # enable output information of  neural network learning progress
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(statistic_report)
    population.add_reporter(neat.Checkpointer(5))
    # run NEAT based on fitness function and amount of birds
    winner = population.run(fitness_function, n=500)
    winner.generation = len(statistic_report.generation_statistics)
    pickle_out = open("..//NEAT//pickle_file//best.pickle", "wb")
    pickle.dump(winner, pickle_out)
    pickle_out.close()


def fitness_function(genomes, config):
    generation_number = len(statistic_report.generation_statistics)
    idx, genomes = zip(*genomes)
    game = GameAppManager(genomes, config)
    game.play(generation_number)
    results = game.crash_info
    top_score = 0
    for result, genomes in results:

        score = result['score']

        fitness = score
        genomes.fitness = -1 if fitness == 0 else fitness
        if top_score < score:
            top_score = score


if __name__ == "__main__":
    main()
