import matplotlib.pyplot as plt

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
