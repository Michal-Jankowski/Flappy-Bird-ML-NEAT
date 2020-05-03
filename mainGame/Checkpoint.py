import neat
import pickle
from modules.GameAppManager import GameAppManager


# mainGame method of train file
# configuration of NEAT algorithm from file
def main():
    global restore
    # restore saved checkpoint
    restore = neat.Checkpointer.restore_checkpoint("../NEAT/checkpoints_file/checkpoint")
    # enable output information of  neural network learning progress
    statistic_report = neat.StatisticsReporter()
    restore.add_reporter(neat.StdOutReporter(True))
    restore.add_reporter(statistic_report)
    restore.add_reporter(neat.Checkpointer(5))

    # run NEAT based on fitness function and amount of birds
    winner = restore.run(fitness_function, n=20)
    pickle_out = open("..//NEAT//pickle_file//best.pickle", "wb")
    pickle.dump(winner, pickle_out)
    pickle_out.close()


def fitness_function(genomes, config):
    generation_number = restore.generation
    idx, genomes = zip(*genomes)
    game = GameAppManager(genomes, config)
    game.play(generation_number)
    results = game.crash_info
    top_score = 0
    for result, genomes in results:

        score = result['score']
        distance = result['distance']

        fitness = score
        genomes.fitness = -1 if fitness == 0 else fitness
        if top_score < score:
            top_score = score


if __name__ == "__main__":
    main()
