import csv
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
                print(len(set(visited)))

    '''for node in all_words_dict:
        for edge in all_words_dict[node]:
            directed_graph.add_edge(node, edge)
    '''
