from collections import namedtuple
from functools import partial
from typing import List, Callable, Tuple
from random import choices, randint, randrange, random
import inline as inline
import matplotlib
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from pandas import DataFrame
import time


class Word:
    def __init__(self, w, visited: bool):
        self.w = w
        self.visited = visited


def print_agraph(graph, source):
    print(f"Source: {source.w}")
    for gr in graph:
        for gr in graph:
            gr.visited = False
        print("==========")
        gr.visited = True
        queue = [gr]
        count = 1
        while len(queue) > 0:
            current = queue.pop()
            current.visited = True
            count += 1
            print(current.w)
            for c in graph[current]:
                if not c.visited:
                    queue.append(c)
        print(count)


if __name__ == '__main__':
    kivi = Word('kivi', False)
    visoki = Word('visoki', False)
    viroza = Word('viroza', False)
    zarazni = Word('zarazni', False)
    niski = Word('niski', False)
    nitrati = Word('nitrati', False)
    virulentni = Word('virulentni', False)

    graph = {kivi: {viroza, visoki},
             viroza: {zarazni, virulentni},
             zarazni: {niski, nitrati},
             niski: {kivi},
             visoki: {kivi},
             nitrati: {},
             virulentni: {niski, nitrati}}

    print_agraph(graph, visoki)
    df_all_words = pd.read_csv('words_filled.csv')
    df_all_words
