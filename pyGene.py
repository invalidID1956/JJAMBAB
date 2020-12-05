import random
import copy


class Entity(object):
    def __init__(self, chromosome):
        self.chromosome: list = chromosome


class Environment(object):
    def __init__(self, entities):
        self.entities = entities
        self.n_of_entities = len(entities)

    def optimize(self, **params):
        selection_f = params["SE_method"]   # returns c1, c2
        crossover_f = params["CV_method"]
        mutation_f = params["MU_method"]
        cost_f = params["cost_function"]
        logging = params["Log"]
        threshold = params["Threshold"]

        current_gen = self.entities

        for k in range(params["epoch"]):
            new_gen = []

            for i in range(self.n_of_entities):
                (e1, e2) = selection_f(current_gen, params)
                e3: Entity = crossover_f((e1, e2), params)
                e3.chromosome = mutation_f(e3, params)
                new_gen.append(e3)

            current_gen = new_gen

            best_chromosome = sorted(current_gen, key=lambda e: cost_f(e.chromosome))[0]
            if cost_f(best_chromosome.chromosome) <= threshold:
                return 1, best_chromosome  # 최적해 도달 완료

            if logging:
                if k % 100 == 0:
                    print(k, "번째 시행: \n", "1) Best Cost: ", cost_f(best_chromosome.chromosome), '\n2) Chromosome: ', best_chromosome.chromosome)

        return 0, best_chromosome


def selection_tournament(generation: list, params: dict):
    result = []
    cost_f = params["cost_function"]
    se_p = params["SE_tournament_p"]

    for _ in range(2):
        Es = [random.choice(generation) for _ in range(2)]

        p = random.random()
        if p > se_p:
            # Cost 높은 순
            reverse = True
        else:
            # Cost 낮은 순
            reverse = False
        r = sorted(Es, key=lambda e: cost_f(e.chromosome), reverse=reverse)[0]
        result.append(r)

    return result


def crossover_uniform(parents: tuple, params: dict):
    cv_p = params["CV_uniform_p"]
    cost_f = params["cost_function"]

    parents = sorted(parents, key=lambda e: cost_f(e.chromosome), reverse=True) # Cost 높은 애가 [0]

    c1: list = parents[0].chromosome
    c2: list = parents[1].chromosome

    result = []

    for g1, g2 in zip(c1, c2):
        k = random.random()
        if k > cv_p:
            result.append(g1)
        else:
            result.append(g2)

    e3: Entity = copy.deepcopy(parents[0])
    e3.chromosome = result

    return e3


def mutation_basic(entity: Entity, params: dict):
    c = entity.chromosome
    mu_p = params['MU_basic_p']
    dna_range: tuple = params['DNA_range']
    result = []
    for d in c:
        k = random.random()
        if mu_p > k:
            result.append(random.randint(*dna_range))
        else:
            result.append(d)
    return result
