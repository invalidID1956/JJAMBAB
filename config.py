import os
import json

from collections import OrderedDict


def main():
    config_file = 'config.json'
    config = OrderedDict()

    if not os.path.exists(os.path.join(os.getcwd(), config_file)):
        print('Configuration not Detected, Creating...')
    else:
        print('Deleting Previous Configuration')
        os.remove(os.path.join(os.getcwd(), config_file))

    print('Input Blank if You Want to Edit Configuration Later.')

    ex_path = input('Input Path to Save Experiment Result and Temp Data: ').replace('~', os.path.expanduser('~'))
    # TODO:  if not LINUX?
    config['EX_HOME'] = ex_path
    data_path = input('Input Path to Read DATA: ').replace('~', os.path.expanduser('~'))
    config['DATA_HOME'] = data_path

    with open(os.path.join(os.getcwd(), config_file), 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent='\t')


if __name__ == '__main__':
    main()