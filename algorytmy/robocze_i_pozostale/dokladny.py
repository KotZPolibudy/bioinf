from dataclasses import dataclass
from typing import List


@dataclass
class Cell:
    posL: int
    posH: int
    data: str


@dataclass
class Param:
    length: int
    start: str
    cells: List[Cell]


def position_error(cell: Cell, position: int, margin: int = 5) -> bool:
    return cell.posL - margin <= position <= cell.posH + margin



def matching(current: str, forMatch: str, position: int) -> bool:
    # Check if the fragment matches at the given position
    for i in range(len(forMatch)):
        if forMatch[i] == "X" or (position + i < len(current) and current[position + i] == forMatch[i]):
            continue
        else:
            print(f"Fragment {forMatch} does not match at position {position}.")
            return False
    print(f"Fragment {forMatch} matches at position {position}.")
    return True





def prepare_to_go_deeper(current: str, forMatch: str, position: int) -> str:
    # Append the matching sequence to the current sequence
    return current + forMatch[position:]


def traverse(current: str, position: int, finished: int, cells: List[Cell]) -> str:
    print(f"Current Sequence: {current}, Position: {position}")

    if len(current) == finished:
        return current

    for i in range(len(cells)):
        if not position_error(cells[i], position, margin=5):
            continue

        print(f"Considering fragment: {cells[i].data}, Positions: {cells[i].posL}-{cells[i].posH}")

        forMatch = cells[i].data
        print(f"Trying fragment: {forMatch}")

        if matching(current, forMatch, position):
            print(f"Fragment {forMatch} matches at position {position}.")
            next_seq = prepare_to_go_deeper(current, forMatch, position)
            print(f"Going deeper with sequence: {next_seq}")
            result = traverse(next_seq, position + len(forMatch), finished, cells)
            if result is not None:
                return result
            else:
                print(f"No valid sequence found with fragment {forMatch} at position {position}.")
                # Reset position if no valid sequence found with this fragment
                position -= len(forMatch)
        else:
            print(f"Fragment {forMatch} does not match at position {position}.")

    return None







def function_to_test(param: Param) -> str:
    length = param.length
    start = param.start
    n_err = int(0.2 * param.length)
    cells = param.cells
    dummycell = "X" * len(start)

    for _ in range(n_err + 1):
        cells.append(Cell(1, 9999999, dummycell))
    cells = sorted(cells, key=lambda x: x.posH)

    return traverse(start, 0, length, cells)


if __name__ == '__main__':
    from parser import parse_xml  # Assuming parse_xml is defined elsewhere

    filepath = "../../data/przyklad_dokladny.xml"
    przyklad = parse_xml(filepath)
    # print(przyklad)

    res = function_to_test(przyklad)
    if res is not None:
        print(f"Success: DNA sequence found: {res}")
    else:
        print("Failure: No DNA sequence could be constructed.")
