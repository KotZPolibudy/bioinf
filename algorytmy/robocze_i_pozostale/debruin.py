import random
import sys
import math
import re
import os
from collections import OrderedDict
from parser import parse_xml


def string_reconstruction(patterns):
    return genome_path(eulerian_path(create_debrujin_graph(patterns), start))


def create_debrujin_graph(patterns):
    k_mers = []
    for temp_pattern in patterns:
        for i in range(len(temp_pattern) - 1):
            k_mers.append(temp_pattern[i:i + len(temp_pattern) - 1])
    k_mers_final = list(OrderedDict.fromkeys(k_mers))

    dict = {}

    for kmer_dict in k_mers_final:
        dict[kmer_dict] = []
    for i in patterns:
        dict[prefix(i)].append(suffix(i))
    return dict


def genome_path(kmers, append_last=True):
    genome = ''
    kmer_length = len(kmers[0])
    for kmer in kmers:
        genome += kmer[0]
    if append_last:
        genome += kmer[-1]
    return genome



def eulerian_path(graph, start):
    stack = []
    path = []
    stack.append(start)

    while stack:
        current_node = stack[-1]
        if graph[current_node]:
            next_node = graph[current_node].pop()
            stack.append(next_node)
        else:
            path.append(stack.pop())
    return path



def suffix(string):
    return string[1:]


def prefix(string):
    return string[:-1]


def function_to_test(dane):
    length = dane.length
    global start
    start = dane.start
    probe = len(start)
    array_oli = [cell.data for cell in dane.cells]

    # Ensure start is a valid k-mer
    if start not in array_oli:
        array_oli.append(start)

    return string_reconstruction(array_oli)[:length]


if __name__ == '__main__':
    filepath = "../../data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)
    res = function_to_test(przyklad)
    print(res)
