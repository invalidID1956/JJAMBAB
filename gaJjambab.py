import pyGene
import openpyxl
import random
import os
import sys
import math

DAYS = 5
N_OF_ENTITIES = 50
DNA_RANGE = (0, 50)
EPOCH = 100

DAILY_NEUT = [
    0, 70, 55, 2700
]   # 탄단지칼

def main(datadir):
    ########################## 엑셀 파일 읽어와서 메뉴 Dictionary 만들기력
    workbook = openpyxl.load_workbook(os.path.join(datadir, 'dishes.xlsx'))
    sheet = workbook.active

    dishes = [[] for _ in range(5)] # 0국 1밥 2반찬 3메인 4특식 5김치

    for sample in sheet.columns:
        type = int(sample[0][0])
        dishes[type].append(
            {
                'code': int(sample[0][1:]),
                'name': sample[1],
                'cost': sample[2],
                'neut': sample[3:6],
                'favor': sample[6]
            }
        )

        result = []
        for type in dishes:
            result.append(
                sorted(type, key=lambda x: x['code'])
            )
        dishes = result

    ########################## Dish Class,CostF 정의
    def cost(menu: list, days=DAYS, w=[0, 0, 0]):
        menus_per_type = [
            [dish[i*5+t] for i in range(days)] for t in range(5)
        ]
        sum_of_neut = sum([
            [dishes[t][d]['neut'] for d in menus_per_type] for t in range(5)
        ])
        sum_of_neut = [
            sum([dish_of_neut[i] for dish_of_neut in sum_of_neut]) for i in range(4) #탄단지칼
        ]
        MSE_of_neut: float = sum([
                (neut-standard_neut*DAYS)**2 for standard_neut in DAILY_NEUT
        ])/(len(menu)*4)

        diversity_of_menus = 0  # 0~4
        for menus in menus_per_type:
            kinds_of_menu = list(set(menus))
            H = 0   # Shannon-Winner Diversity
            for kind in kinds_of_menu:
                p = menus.count(kind)/len(menus)
                H -= p*math.log(p, math.e)
            diversity_of_menus += H
        diversity_of_menus = diversity_of_menus/5   #Types

        sum_of_unlikely = 0
        for t, m in enumerate(menus_per_type):
            sum_of_unlikely += (dishes[t][m]['likely']-5)**2
        mean_of_unlikely = sum_of_unlikely/len(menu)

        return w[0]*MSE_of_neut + w[1]*diversity_of_menus + w[2]*mean_of_unlikely

    class Menu(pyGene.Entity):
        def __init__(self, chromosome, days=DAYS):
            self.days = days
            super().__init__(chromosome)

    gen = []
    for i in range(N_OF_ENTITIES):
        gen.append(
            Menu(
                [random.randint(*DNA_RANGE) for _ in range(N_OF_ENTITIES)]
            )
        )


    ######################### params 정의, Optimizer 작동

    environment = pyGene.Environment(gen)
    environment.optimize(
        epoch=EPOCH,
        cost_function=cost,
        SE_method=pyGene.selection_tournament,
        SE_tournament_p=0.8,
        CV_method=pyGene.crossover_uniform,
        CV_uniform_p=0.8,
        MU_method=pyGene.mutation_basic,
        MU_basic_p=0.05,
        DNA_range=DNA_RANGE,
        Log=True,
        Threshold=0.05
    )

    ######################### 결과 엑셀로 출

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)