import pickle
import os

import pyGene

##


class Dish(object):
    def __init__(self, dict):
        self.type = dict['type']
        self.code = dict['code']
        self.cost = dict['cost']
        self.neut = dict['neut']
        self.likely = dict['likely']


def loss(weigh: list, ):
    weigh[0]*