from dataclasses import dataclass, asdict
import itertools


@dataclass
class Cell:
    posL: int
    posH: int
    data: str


def make_all_possible_of_len_n_dict(oligo_len):
    return {''.join(word): [] for word in itertools.product("ACTG", repeat=oligo_len)}


def build_sequence(start, maindict, oligo_len):
    sequence = start
    while True:
        last_n_minus_1 = sequence[-(oligo_len - 1):]
        if last_n_minus_1 in maindict and maindict[last_n_minus_1]:
            next_cell = maindict[last_n_minus_1].pop(0)
            sequence += next_cell.data[-1]
        else:
            break
    return sequence


def function_to_test(param):
    length = param.length
    start = param.start
    cells = param.cells
    n = len(start)
    maindict = make_all_possible_of_len_n_dict(n - 1)
    for cell in cells:
        maindict[cell.data[0:-1]].append(cell)

    # Build the sequence starting from the initial fragment
    sequence = build_sequence(start, maindict, n)

    return sequence


if __name__ == '__main__':
    from parser import parse_xml

    filepath = "data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)

    res = function_to_test(przyklad)
    print(res)
