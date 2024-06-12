from collections import defaultdict
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


def eulerian_path(graph, start):
    stack = []
    path = []

    current = start
    stack.append(current)

    while stack:
        if graph[current]:
            next_node = graph[current].pop()
            stack.append(next_node)
            current = next_node
        else:
            path.append(stack.pop())
            if stack:
                current = stack[-1]
    return path[::-1]


def function_to_test(dane):
    array_oli = [cell.data for cell in dane.cells]
    start = dane.start

    graph = create_debrujin_graph(array_oli)
    path = eulerian_path(graph, start)
    return genome_path(path)


if __name__ == '__main__':
    filepath = "../../data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)
    res = function_to_test(przyklad)
    print(res)
