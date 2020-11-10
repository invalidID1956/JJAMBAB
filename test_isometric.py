import pyGene
import random


def cost(chromosome: list):
    result = 0
    target = [2**k for k in range(10)]
    for c, t in zip(chromosome, target):
        if c != t:
            result += 1
    return result


n_of_entities = 100
len_of_chromosome = 10
dna_range = (0, 2000)

initial_gen = [pyGene.Entity([random.randint(*dna_range) for _ in range(len_of_chromosome)])
               for __ in range(n_of_entities)]

environment = pyGene.Environment(
    entities=initial_gen
)

reached, optimized = environment.optimize(
    epoch=50000,
    cost_function=cost,
    SE_method=pyGene.selection_tournament,
    SE_tournament_p=0.8,
    CV_method=pyGene.crossover_uniform,
    CV_uniform_p=0.8,
    MU_method=pyGene.mutation_basic,
    MU_basic_p=0.05,
    DNA_range=dna_range,
    Log=True,
    Threshold=0
)
