'''
염색체는 0과 1로 이루어진 길이 10의 수열,
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]에 가까울수록 점수가 높다.
'''

import pyGene
import random

n_of_en = 50
epoch = 5000


def cost(gene):
    c = 0
    target = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    for dna, t_dna in zip(gene.gene, target):
        if dna !=t_dna:
            c+=1
    return c


def repair(gene):
    g = gene
    for dna in g:
        if (dna!=0) and (dna!=1):
            dna = random.choice((1, 0))
    return g # 확인요

gen = []
for i in range(n_of_en):
    gen.append([random.choice((0, 1)) for _ in range(10)])

env = []
for chr in gen:
    env.append(
        pyGene.Entity(
            gene=chr,
            repair=repair,
        )
    )

Env = pyGene.Environment(initial_entities=env)

gen = Env.optimize(cost_function=cost, epoch=epoch)

print(gen[0].gene)