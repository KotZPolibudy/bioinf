from collections import defaultdict
from parser import parse_xml


def create_debrujin_graph(patterns):
    dict = defaultdict(list)

    k_mers = {pattern[:-1] for pattern in patterns}

    for pattern in patterns:
        dict[pattern[:-1]].append(pattern[1:])

    return dict


def genome_path(kmers, append_last=True):
    genome = ''.join(kmer[0] for kmer in kmers)
    if append_last:
        genome += kmers[-1][1:]
    return genome


def eulerian_path(graph, start):
    stack = []
    path = []

    temp_start = start[:-1]

    temp_stack1 = {key: val for key, val in graph.items()
                   if key.startswith(temp_start)}

    temp_key = list(temp_stack1.keys())
    temp_value = list(temp_stack1.values())

    stack.append(temp_key[0])
    stack.append(temp_value[0][0])

    w = temp_value[0][0]

    graph[temp_start].remove(w)

    while stack:
        u_v = stack[-1]
        try:
            w = graph[u_v][0]
            stack.append(w)
            graph[u_v].remove(w)
        except IndexError:
            path.append(stack.pop())
    return path[::-1]


def function_to_test(filepath):
    przyklad = parse_xml(filepath)
    length = przyklad.length
    start = przyklad.start
    probe = len(start)
    array_oli =  [cell.data for cell in przyklad.cells]


    graph = create_debrujin_graph(array_oli)
    path = eulerian_path(graph, start)
    return genome_path(path)


if __name__ == '__main__':
    res = function_to_test('data/przyklad_dokladny.xml')
    print(res)