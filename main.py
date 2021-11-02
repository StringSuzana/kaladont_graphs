import matplotlib.pyplot as plt
import csv
import networkx as nx
import string
import itertools
import ast
from collections import deque

graph = {}


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


def has_path(graph, source, destination):  # Directed acyclic graph
    if source == destination:
        return True
    for neighbour in graph[source]:
        if has_path(graph, neighbour, destination):
            return True
    return False


def bfs(source, destination):
    visited = set()
    queue = deque()  # Init a queue= deque(),add= append(), remove= popleft()
    queue.append(source)
    while len(queue) > 0:
        current = queue.popleft()
        visited.add(current)
        if current == destination:
            print('=====FOUND IT======')
            print(visited)
        destinations = graph[current]
        for dest in destinations:
            if dest not in visited:
                queue.append(dest)


def dfs_recursive(start, visited=set()):
    print(start)
    visited.add(start)
    destinations = graph[start]
    for dest in destinations:
        if dest == 'kalodont':
            print(f'found kalodont in steps: ')
            return
        if dest not in visited:
            dfs_recursive(dest, visited)
    print('=================REACHED THE LEAF NODE=================')
    return


def dfs_recursive_modified(start, visited=[]):
    print(start)
    if len(visited) > 0:
        if visited[len(visited) - 1][-2:] != start[0:2]:
            print("should have returned the visited : ")
            return visited
    visited.append(start)
    destinations = graph[start]
    for dest in itertools.islice(destinations, 10):
        if dest == 'kalodont':
            print(f'found kalodont in steps: ')
            return
        if dest not in visited:
            dfs_recursive_modified(dest, visited)
        print('=================REACHED THE LEAF NODE=================')
    return


def dfs_modified(rand_sort, start, visited_list=[]):
    # visited_list.append(start)
    stack = deque()  # Init stack for a while loop
    stack.append(start)  # Push starting node to stack

    while len(stack) > 0:
        current = stack.pop()  # From the TOP of the stack
        if len(visited_list) > 0:
            if visited_list[len(visited_list) - 1][-2:] != current[0:2]:
                if len(visited_list) > 1:
                    return visited_list[:-1]

        if current not in visited_list:
            visited_list.append(current)
            destinations = graph[current]
            # print(current)

            for dest in sorted(destinations, reverse=rand_sort):
                if dest not in visited_list:
                    stack.append(dest)
    return []



def dfs(graph, start, visited=set()):
    visited_list = [start]  # Add starting node to visited set
    stack = deque()  # Init stack for a while loop
    stack.append(start)  # Push starting node to stack

    while len(stack) > 0:
        current = stack.pop()  # From the TOP of the stack
        visited_list.append(current)
        destinations = graph[current]
        print(current)

        for dest in destinations:
            if dest not in visited_list:
                stack.append(dest)

    print('========================END========================')


def small_graph():
    small_graph_dict = dict(kivi={'visoki', 'viroza'},
                            viroza={'zarazni'},
                            zarazni={'niski', 'nitrati', 'niti'},
                            niski={'kivi'},
                            visoki={'kivi'},
                            nitrati={'tikovina'},
                            virulentni={'niski', 'nitrati'},
                            tikovina=set(),
                            niti={'tikovina'})
    graph = small_graph_dict
    dfs(small_graph_dict, 'kivi')
    # e = next(iter(graph))
    # print(e.startswith('Ki'.casefold()))
    # dfs(visited_set, graph, 'kivi')


if __name__ == '__main__':
    with open('ending_letters_dict.txt', 'r') as f:
        ser = f.read()
    ending_letters_dict = set() if ser == str(set()) else ast.literal_eval(ser)

    all_words_dict = {}
    with open('words_filled.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        words = []
        for row in reader:  # 0=index, 1=text, 2=starting letters, 3=ending_letters
            # Create dict item like=> 'kivi': {'visoki', 'viroza'}
            all_words_dict[row[1]] = ending_letters_dict.get(row[3], set())  # If not exists, return empty set()
    graph = all_words_dict

    for every_word in all_words_dict:
        GAME_OVER = False
        starting_word = every_word
        visited = [starting_word]
        print(starting_word)
        toggle: bool = False
        while not GAME_OVER:
            toggle = not toggle
            new_visited = dfs_modified(toggle, starting_word, visited)
            if len(new_visited) > 0:
                starting_word = new_visited.pop()
                if len(new_visited) > 0:
                    visited.extend(new_visited)

            else:
                GAME_OVER = True
                if (len(visited) > 10_000) & (len(visited) == len(set(visited))):
                    print(visited)
                print(len(set(visited)))

    '''for node in all_words_dict:
        for edge in all_words_dict[node]:
            directed_graph.add_edge(node, edge)
    '''


def writing_ending_letters():
    ending_letters = set()
    with open('words_filled.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            # 0 index, 1 rijec, 2, pocetna slova, 3 zavrsna slova
            ending_letters.add(row[3])

    print(len(ending_letters))
    with open('ending_letters.txt', 'w') as f:
        f.write(str(ending_letters))

    ending_letters_dict = dict()
    for last_two_letters in ending_letters:
        with open('words_filled.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',')
            set_of_connecting_words = set()
            for row in reader:
                if row[2] == last_two_letters:
                    set_of_connecting_words.add(row[1])
            ending_letters_dict[last_two_letters] = set_of_connecting_words

    print(ending_letters_dict)
    with open('ending_letters_dict.txt', 'w') as f:
        f.write(str(ending_letters_dict))


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


def reading_file_words_objects():
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


def playing_with_word_objects():
    kivi = Word('kivi', False, 'vi')
    visoki = Word('visoki', False, 'ki')
    viroza = Word('viroza', False, 'za')
    zarazni = Word('zarazni', False, 'ni')
    niski = Word('niski', False, 'ki')
    nitrati = Word('nitrati', False, 'ti')
    virulentni = Word('virulentni', False, 'ni')
    tikovina = Word('tikovina', False, 'na')

    graph_objects = {kivi: set([visoki, viroza]),
                     viroza: set([zarazni]),
                     zarazni: set([niski, nitrati]),
                     niski: set([kivi]),
                     visoki: set([kivi]),
                     nitrati: set([tikovina]),
                     virulentni: set([niski, nitrati]),
                     tikovina: set()}


def print_a_graph(visited: set(), graph, source):
    # This is not working properly
    print("==========")
    print(f"Source: {source}")
    visited_list.append(source)
    for node in graph:
        queue = [source]
        while len(queue) > 0:
            current = queue.pop()
            print(current)
            visited.add(current)
            for c in graph[current]:
                if c not in visited:
                    queue.append(c)
