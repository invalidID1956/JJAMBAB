import pyGene
import openpyxl
import random
import os
import sys
import math


DAYS = 10
N_OF_ENTITIES = 5*DAYS
DNA_RANGE = (1, 48)
EPOCH = 50000

DAILY_NEUT = [
    130, 70, 55, 2700
]   # 탄단지칼

def main(datadir, outfile):
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
    def cost(menu: list, days=DAYS, w=[0.001, 1, 0.5]):
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

        return w[0]*MSE_of_neut - w[1]*diversity_of_menus + w[2]*mean_of_unlikely

    class Menu(pyGene.Entity):
        def __init__(self, chromosome, days=DAYS, database = dishes):
            self.days = days
            self.database = database
            super().__init__(chromosome)

        def interpret(self):
            result = []
            for i, gene in enumerate(self.chromosome):
                type = i%5   # 0국 1밥 2반찬 3메인 4특식
                result.append(
                    self.database[type][gene]['name']
                )
                if type==4:
                    result.append('\SEP')

            r = []
            temp = []
            for m in result:
                if m!='\SEP':
                    temp.append(m)
                else:
                    temp.append(random.choice(['배추김치', '파김치']))
                    r.append(temp)
                    temp = []

            return r



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
        SE_tournament_p=0.8,
        CV_method=pyGene.crossover_uniform,
        CV_uniform_p=0.7,
        MU_method=pyGene.mutation_basic,
        MU_basic_p=0.05,
        DNA_range=DNA_RANGE,
        Log=True,
        Threshold=3.0
    )

    ######################### 결과 엑셀로 \

    f =  final_dish.interpret();
    sheet = []

    menus_per_week = []
    temp = []
    for i, menu in enumerate(f):
        temp.append(menu)
        if i%5==4 :  # DAYS는 5의 배수
            menus_per_week.append(temp)
            temp = []

    for w, weekly in enumerate(menus_per_week):
        sheet.append([w*5 +i+1 for i in range(5)])
        for i in range(4):
            sheet.append([daily[i] for daily in weekly])

    wb = openpyxl.Workbook()
    ws = wb.active

    for line in sheet:
        print(line)
        ws.append(line)

    wb.save(outfile)
    
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
            ''' # 클래스 내에 번역 메서드

if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)

