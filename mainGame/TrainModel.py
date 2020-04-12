import neat
import pickle
from modules.GameAppManager import GameAppManager


# mainGame method of train file
# configurate NEAT algorithm from file
def main():
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        '../NEAT/config/feedforward-config'
    )
    # set population of bird
    p = neat.Population(config)
    # enable output information of  neural network learning progress
    p.add_reporter(neat.StdOutReporter(True))
    # run NEAT based on fitness function and amount of birds
    winner = p.run(eval_genomes, n=50)
    pickle_out = open("best.pickle", "wb")
    pickle.dump(winner, pickle_out)
    pickle_out.close()

def eval_genomes(genomes, config):
    idx, genomes = zip(*genomes)
    game = GameAppManager(genomes, config)
    game.play()
    results = game.crash_info
    top_score = 0
    for result, genomes in results:

        score = result['score']
        distance = result['distance']

        fitness = distance
        genomes.fitness = -1 if fitness == 0 else fitness
        if top_score < score:
            top_score = score

    # print("Highest Score:", top_score)


if __name__ == "__main__":
    main()
