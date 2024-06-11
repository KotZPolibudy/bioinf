from dataclasses import dataclass, asdict


@dataclass
class Cell:

    posL: int
    posH: int
    data: str


def function_to_test(param):
    length = param.length
    start = param.start
    n_err = 0.2 * param.length
    cells = param.cells
    dummycell = "X" * len(start)
    for i in range(int(n_err) + 1):
        cells.append(Cell(1, 9999999, dummycell))
    cells = sorted(cells, key=lambda x: x.posH)

    # krok 3,




    return cells


if __name__ == '__main__':
    from parser import parse_xml

    filepath = "data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)

    res = function_to_test(przyklad)
    print(res)
