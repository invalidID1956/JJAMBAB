import random


def crossover_uniform(g1, g2, k):
    '''
    :param g1: Mother Gene
    :param g2: Father Gene
    :param k: Threshold Probability (0<k<1)
    :return: Offspring Gene
    '''
    result = []
    if len(g1)==len(g2):
        for d1, d2 in zip(g1, g2):
            p = random.random()
            if p>k:
                result.append(d1)
            else:
                result.append(d2)
        return result

    else:
        print('Warning: Chromosome Length are Different')
        return g1


def crossover_singlepoint(g1,g2, k):
    pass


def crossover_multipoint(g1, g2, k):
    pass


def selection_tournament(entities, p, cost):
    def tournament():
        g1 = random.choice(entities)
        g2 = random.choice(entities)

        k = random.random()

        if p > k:
            if cost(g1) > cost(g2):
                return g1
            else:
                return g2
        else:
            if cost(g1) > cost(g2):
                return g2
            else:
                return g1

    r1 = tournament()
    r2 = tournament()

    return r1, r2


def selection_roulette(entities, p, cost):
    pass


def mutation_basic(chromosome: list, p, dnarange):
    result = []
    for dna in chromosome:
        k = random.random()
        if p>k:
            d = random.randint(*dnarange)
        else:
            d = dna
        result.append(d)

    return result


def mutation_non_uniform(chromosome, p):
    pass


def repair_basic(chromosome):
    return chromosome


# 생성 -> 변이+repair -> __add__로 교차 수행 후 딸세포 남기고 퇴
class Entity(object):
    def __init__(self, gene: list, dna_range, repair=repair_basic, crossover_method=crossover_uniform, crossover_k=0.5, mutation=mutation_basic,  mutation_p=0.01):
        self.crossover_method = crossover_method
        self.crossover_k = crossover_k
        self.repair = repair
        self.mutation = mutation
        self.mutation_p = mutation_p
        self.dna_range = dna_range

        self.gene = repair(mutation(gene, mutation_p, dna_range))

    def __add__(self, other):
        return Entity(gene=self.crossover(self.gene, other.gene),
                      repair=self.repair,
                      mutation=self.mutation,
                      dna_range=self.dna_range
                      )  # TODO: 나머지 인자도 다 채우기, 근데 차피 이거 오버로딩할거임

    def crossover(self, a, b):
        return self.crossover_method(a, b, self.crossover_k)


class Environment(object):
    def __init__(self, initial_entities: list):
        self.n_of_entities = len(initial_entities)
        self.entities = initial_entities

    def optimize(self, cost_function, epoch: int, selection=selection_tournament, selection_p=0.1):
        gen = self.entities

        for i in range(epoch):
            next_gen = []
            for n in range(self.n_of_entities):
                g1, g2 = selection(entities=gen, p=selection_p, cost=cost_function)
                new_g = g1+g2
                next_gen.append(new_g)
            gen = next_gen
            print(i, '번째', gen[0].gene)

        return gen
