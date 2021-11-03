import csv
import string
import itertools
import ast
from collections import deque
import random
import time

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


def get_weight(target_set: set(), visited_list: []) -> int:
    # print(len(target_set))
    target_set.discard(set(visited_list))
    # print(len([x for x in target_set if x not in visited_list]))  # Also ok
    return len(target_set)


def dfs_modified(start, visited_list=[]):
    stack = deque()  # Init stack for a while loop
    stack.append(start)  # Push starting node to stack

    while len(stack) > 0:

        current = stack.pop()  # From the TOP of the stack

        if current not in visited_list:
            if len(
                    visited_list) > 0:  # Ovo znaci da je krenuo na novu granu traziti u dubinu a to sam odlucila zanemariti
                if (visited_list[len(visited_list) - 1][-2:] != current[0:2]) & (current != start):
                    return visited_list
            # Ako nije krenuo na novu granu nego nastavlja put niz prvu niz koju je krenuo:

            # Osim ako se trenutna rijec ne moze povezati na barem dvije
            if len(graph.get(current) - set(visited_list)) < 2:
                continue

            visited_list.append(current)
            #print(len(visited_list))
            destinations = graph[current]  # Sve nadovezive rijeci od TRENUTNO VISITED rijeci:
            destination_half_sample = random.sample(list(destinations), k=(
                int(len(destinations) / 2)))  # mejbi pretvorit u listu destinations?
            if len(destination_half_sample) < 100:
                destination_half_sample = destinations
            # print(current)
            # for dest in sorted(destinations, reverse=rand_sort): 200-400
            # Sortirat destinations po tome koliko oni u graph[dest] imaju spojnih destinacija (koje nisu u visited? => to je ekstra effort)
            # wanted = lambda w: len(graph.get(w))
            # lambda w: len(graph.get(w).discard(set(visited_list)))
            # lambda w: len([x for x in graph.get(w) if x not in visited_list]) # ULTRA sporo 0.59000253...0.19998931
            # lambda w: get_weight(graph.get(w), visited_list) 0.016001701...0.0130000114
            # lambda w: len(graph.get(w)- set(visited_list)) 0.088975191 ...0.058000326156
            # before_sort = time.time()
            test = sorted(destination_half_sample, key=lambda w: len(graph.get(w)),
                          reverse=False)
            # after_sort = time.time()
            # print(f"Sort time: {after_sort - before_sort}")

            # bla = [dest for dest in test[int(len(test) / 2):] if dest not in visited_list]
            for a in test:
                stack.append(a)

    return visited_list


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
        visited = []
        # visited.append(starting_word) NO BECAUSE OF THE DFS FUNCTION IMPLEMENTATION
        print(f"STARTING WITH NEW WORD: {starting_word}")
        guarding_value=0
        count = 0
        dfs_result_visited = []
        while not GAME_OVER:
            print(f"Visited len BEFORE entering dfs func: {len(visited)}")
            dfs_result_visited = dfs_modified(starting_word, visited[:])
            if len(dfs_result_visited) > (len(
                    visited) + 1):  # Zbog toga sto sam sigurna da cu barem starting word staviti u visited unutar funkcije dfs
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                dfs_result_visited.pop()
                starting_word = dfs_result_visited.pop()
                visited = dfs_result_visited[:]
                print(f"Change starting_word to: {starting_word}")
                print(
                    f"Visited len after starting_word change: {len(visited)}, dfs_result_visited len: {len(dfs_result_visited)} ")
                if guarding_value == 0:
                    guarding_value = len(visited)
                elif len(visited)<guarding_value:
                    GAME_OVER = True
            else:
                GAME_OVER = True
                print(f"Visited len after GAME_OVER: {len(visited)}")

    '''for node in all_words_dict:
        for edge in all_words_dict[node]:
            directed_graph.add_edge(node, edge)
    '''
