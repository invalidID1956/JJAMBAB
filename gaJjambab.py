import pyGene
import openpyxl
import random
import os
import sys
import math

DAYS = 10
N_OF_ENTITIES = 5*DAYS
DNA_RANGE = (1, 48)
EPOCH = 100000

DAILY_NEUT = [
    0, 70, 55, 2700
]   # 탄단지칼

def main(datadir):
    ########################## 엑셀 파일 읽어와서 메뉴 Dictionary 만들기력
    workbook = openpyxl.load_workbook(os.path.join(datadir, 'dishes.xlsx'))
    sheet = workbook.active

    dishes = [[] for _ in range(6)] # 0국 1밥 2반찬 3메인 4특식 5김치

    for sample in sheet.rows:
        type = int(int(sample[0].value)/1000)
        dishes[type].append(
            {
                'code': int(sample[0].value),
                'name': sample[1].value,
                'cost': sample[2].value,
                'neut': [s.value for s in sample[3:7]],
                'favor': sample[7].value
            }
        )


        result = []
        for type in dishes:
            result.append(
                sorted(type, key=lambda x: x['code'])
            )
        dishes = result

    ########################## Dish Class,CostF 정의
    def cost(menu: list, days=DAYS, w=[0.001, 2, 0.5]):
        menus_per_type = [
            [dishes[t][menu[i*5+t]] for i in range(days)] for t in range(5)
        ]

        sum_of_neut = sum([
            [d['neut']  for d in menus_per_type[t]] for t in range(5)
        ], [])

        sum_of_neut = [
            sum([dish_of_neut[i] for dish_of_neut in sum_of_neut]) for i in range(4) #탄단지칼
        ]
        MSE_of_neut: float = math.sqrt(sum([
                (neut-standard_neut*DAYS)**2 for neut, standard_neut in zip(sum_of_neut, DAILY_NEUT)
        ])/(len(menu)*5*4))

        diversity_of_menus = 0  # 0~4
        for menus in menus_per_type:
            kinds_of_menu = []
            for menu in menus:
                if menu in kinds_of_menu:
                    continue
                else:
                    kinds_of_menu.append(menu)

            H = 0   # Shannon-Winner Diversity
            for kind in kinds_of_menu:
                p = menus.count(kind)/len(menus)
                H -= p*math.log(p, math.e)
            diversity_of_menus += H
        uniformity_of_menus = 4-diversity_of_menus/5   #Types

        sum_of_unlikely = 0
        for dish in menus_per_type:
            for d in dish:
                sum_of_unlikely += (d['favor']-5)**2
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

    checker, final_dish = environment.optimize(
        epoch=EPOCH,
        cost_function=cost,
        SE_method=pyGene.selection_tournament,
        SE_tournament_p=0.85,
        CV_method=pyGene.crossover_uniform,
        CV_uniform_p=0.85,
        MU_method=pyGene.mutation_basic,
        MU_basic_p=0.05,
        DNA_range=DNA_RANGE,
        Log=False,
        Threshold=2.0
    )

    ######################### 결과 엑셀로 \

    file = "/result_dishes.xlsx"
    wb = openpyxl.Workbook()

    dishes_per_day = []

    for _ in final_dish:
        r = []
        for i in range(5):
            r.append(final_dish.pop(-1))
        dishes_per_day.append(r)
    print(dishes_per_day)

    item = []
    for i, d in enumerate(dishes_per_day):
        print(i)
        item.append(
            [[i]+[dishes[k][d[k]]['name']  for k in range(5)]+ [dishes[5][0]['name'] ]]
        )

    # sheet = wb.get_sheet_by_name('RESULT')

    '''
    for i in range(DAYS): # 날짜/국/밥/반찬/메인/특식/김치
        week = int(i/5)
        for day, dish in enumerate(dishes_per_day):
            sheet(
                row=week*6,
                column=
            )

            for m, menu in enumerate(dish):
                sheet(
                    row = week*6+(m+1),

                )
            '''

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)

