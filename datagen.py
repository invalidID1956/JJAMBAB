import openpyxl
import sys
import os
import pickle


def main(datadir, file):
    workbook = openpyxl.load_workbook(os.path.join(datadir, file))
    sheet = workbook.active

    dishes = []

    for sample in sheet.columns:
        dish = {
            'code': sample[0],
            'type': sample[0][0],
            'name':sample[1],
            'cost': sample[2],
            'neut': sample[3:6],
            'likely': sample[6]
        }
        dishes.append(dish)

        # TODO: EX_HOME으로 나가
        with open('dishes.p', 'wb') as f:
            pickle.dump(dishes, f)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(*args)


'''
INPUT: datagen.py $DATA_HOME DATA
OUTPUT: JSON
'''