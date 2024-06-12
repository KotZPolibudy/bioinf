from collections import defaultdict, Counter
from parser import parse_xml


def create_debrujin_graph(patterns):
    graph = defaultdict(list)

    for pattern in patterns:
        prefix = pattern[:-1]
        suffix = pattern[1:]
        graph[prefix].append(suffix)

    return graph


def genome_path(kmers, append_last=True):
    genome = ''.join(kmer[0] for kmer in kmers)
    if append_last:
        genome += kmers[-1][1:]
    return genome


def find_unbalanced_nodes(graph):
    out_degree = Counter()
    in_degree = Counter()

    for node, neighbors in graph.items():
        out_degree[node] += len(neighbors)
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    start = end = None
    for node in set(out_degree.keys()).union(set(in_degree.keys())):
        out = out_degree[node]
        inp = in_degree[node]

        if out > inp:
            start = node
        elif inp > out:
            end = node

    return start, end


def eulerian_path(graph, start):
    stack = [start]
    path = []

    while stack:
        current = stack[-1]

        if graph[current]:
            next_node = graph[current].pop()
            stack.append(next_node)
        else:
            path.append(stack.pop())

    return path[::-1]


def function_to_test(dane):
    array_oli = [cell.data for cell in dane.cells]
    poczatek = dane.start
    graph = create_debrujin_graph(array_oli)

    start_prefix = poczatek[:-1]
    path = eulerian_path(graph, start_prefix)

    return genome_path(path)


if __name__ == '__main__':
    filepath = "../../data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)
    res = function_to_test(przyklad)
    print(res)
