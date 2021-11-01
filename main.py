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
import csv
import networkx as nx
import string
import itertools
import scipy as sp


class Word:
    def __init__(self, text, visited: bool, ending_letters: string):
        self.connect_to_set = set()
        self.text = text
        self.visited = visited
        self.ending_letters = ending_letters

    def add_to_set(self, word_to_add):
        self.connect_to_set.add(word_to_add)

    def print_set_of_connecting_words(self):
        for w in self.connect_to_set:
            print(w.text)


def print_a_graph(graph):
    for gr in graph:
        if gr.text == 'acimac':
            print(f"Source: {gr.text}")
            '''for g in graph:
                g.visited = False'''
            print("==========")
            gr.visited = True
            queue = [gr]
            count = 0
            while len(queue) > 0:
                current = queue.pop()
                print(current.text)
                current.visited = True
                count += 1
                for c in current.connect_to_set:
                    if not c.visited:
                        queue.append(c)
            print(f"Source: {gr.text}, Breadth: {count - 1}, connecting words for source: {len(gr.connect_to_set)}")


def drawing_graph(list_of_words: [Word]):
    directed_graph = nx.DiGraph()
    for node in list_of_words:
        for edge in node.connect_to_set:
            directed_graph.add_edge(node.text, edge.text)
    nx.draw(directed_graph, with_labels=True)
    plt.show()
    # G.add_edges_from([('kivi', 'viroza'), ('kivi', 'visoki')])
    # print(G.nodes())
    # print(G.edges().data())


if __name__ == '__main__':
    kivi = Word('kivi', False, 'vi')
    visoki = Word('visoki', False, 'ki')
    viroza = Word('viroza', False, 'za')
    zarazni = Word('zarazni', False, 'ni')
    niski = Word('niski', False, 'ki')
    nitrati = Word('nitrati', False, 'ti')
    virulentni = Word('virulentni', False, 'ni')

    graph = {'kivi': {'viroza', 'visoki'},
             'viroza': {'zarazni', 'virulentni'},
             'zarazni': {'niski', 'nitrati'},
             'niski': {'kivi'},
             'visoki': {'kivi'},
             'nitrati': {},
             'virulentni': {'niski', 'nitrati'}}
    e = next(iter(graph))
    # print(e.startswith('Ki'.casefold()))

    graph_objects = {kivi: set([viroza, visoki]),
                     viroza: set([zarazni, virulentni]),
                     zarazni: set([niski, nitrati]),
                     niski: set([kivi]),
                     visoki: set([kivi]),
                     nitrati: set([]),
                     virulentni: set([niski, nitrati])}
    # Napravi listu rijeci (objekti word klase)
    # za svaku rijec prodi kroz listu rijeci i napravi dictionary od tog

    with open('words_filled.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        words = []
        for row in itertools.islice(reader, 500):
            # print(row)
            # 0 index, 1 rijec, 2, pocetna slova, 3 zavrsna slova
            word = Word(row[1], False, row[3])
            words.append(word)
        for word_item in words:
            for w in words:
                if w.text.startswith(word_item.ending_letters):
                    word_item.add_to_set(w)

    print_a_graph(words)

    # G.add_node(word)
