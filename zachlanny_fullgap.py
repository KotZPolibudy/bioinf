from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Cell:
    posL: int
    posH: int
    data: str


@dataclass
class Params:
    key: int
    length: int
    start: str
    cells: List[Cell]


def fits(sequence, newcell, cell_len, gap):
    if gap >= cell_len:
        return True
    # check if the posL and posH match
    pomseq = sequence[-(cell_len - gap):]
    pomnew = newcell.data[:cell_len - gap]
    if pomnew == pomseq:
        # print("yes")
        return True
    else:
        # print("no")
        return False


def function_to_test(param):
    length = param.length
    start = param.start
    cells = sorted(param.cells, key=lambda x: x.posH)
    cell_length = len(start)
    seq = start

    while cells and len(seq) < length:
        found = False
        for gap in range(1, cell_length + 1):
            j = 0
            while j < len(cells):
                if fits(seq, cells[j], cell_length, gap):
                    seq += cells[j].data[-gap]
                    cells.pop(j)
                    found = True
                    break
                j += 1
            if found:
                break
    return seq


if __name__ == '__main__':
    from parser import parse_xml

    filepath = "data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)
    res = function_to_test(przyklad)
    print(res)
