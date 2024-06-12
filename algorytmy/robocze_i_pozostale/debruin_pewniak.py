import random
import sys
import math
import re
import os
from collections import OrderedDict
from parser import parse_xml


def string_reconstruction(patterns):
    return genome_path(eulerian_path(create_debrujin_graph(patterns)))


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


def genome_path(kmers, apppend_last=True):
    genome = ''
    kmer_length = len(kmers[0])
    for kmer in kmers:
        genome += kmer[0]
    if apppend_last:
        genome += kmer[1:]
    return genome


def eulerian_path(dict):
    stack = []
    path = []

    temp_start = start[:len(start) - 1]

    temp_stack1 = {key: val for key, val in dict.items()
                   if key.startswith(temp_start)}

    temp_key = list(temp_stack1.keys())
    temp_value = list(temp_stack1.values())

    stack.append(temp_key[0])
    stack.append(temp_value[0][0])

    w = str(temp_value[0][0])

    dict[temp_start].remove(temp_value[0][0])

    while stack != []:
        u_v = stack[-1]
        try:
            w = dict[u_v][0]
            stack.append(w)
            dict[u_v].remove(w)
        except:
            path.append(stack.pop())
    return path[::-1]


def suffix(string):
    return string[1:]


def prefix(string):
    return string[0:-1]


def function_to_test(dane):
    length = dane.length
    global start
    start = dane.start
    probe = len(start)
    array_oli = [cell.data for cell in dane.cells]
    size = length - probe + 1

    return string_reconstruction(array_oli)


if __name__ == '__main__':
    filepath = "../../data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)
    res = function_to_test(przyklad)
    print(res)
