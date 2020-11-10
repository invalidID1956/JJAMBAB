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
    target = [3*i for i in range(50)]
    for dna, t_dna in zip(gene.gene, target):
        if dna !=t_dna:
            c+=1
    return c


def repair(gene):
    g = gene
    for dna in g:
        if not (0<=dna<=150):
            dna = random.choice((1, 0))
    return g # 확인요

gen = []
for i in range(n_of_en):
    gen.append([random.randint(0, 150) for _ in range(50)])

env = []
for chr in gen:
    env.append(
        pyGene.Entity(
            gene=chr,
            repair=repair,
            dna_range=(0, 150)
        )
    )

Env = pyGene.Environment(initial_entities=env)

gen = Env.optimize(cost_function=cost, epoch=epoch)

print(gen[0].gene)