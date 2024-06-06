import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Cell:
    posL: int
    posH: int
    data: str


@dataclass
class DNA:
    key: int
    length: int
    start: str
    cells: List[Cell]


def parse_xml(file_path: str) -> DNA:
    tree = ET.parse(file_path)
    root = tree.getroot()

    key = int(root.attrib['key'])
    length = int(root.attrib['length'])
    start = root.attrib['start']

    cells = []
    for cell in root.find('probe').findall('cell'):
        posL = int(cell.attrib['posL'])
        posH = int(cell.attrib['posH'])
        data = cell.text
        cells.append(Cell(posL, posH, data))

    return DNA(key=key, length=length, start=start, cells=cells)


def main():
    # Path to the XML file
    file_path = 'data/przyklad2.xml'
    dna = parse_xml(file_path)

    # Print the parsed data
    print("len: ", dna.length)
    print("start: ", dna.start)
    #print(dna.cells)
    for cell in dna.cells:
        #print(cell)
        #print(asdict(cell))
        print("posL : {} posH: {}, data: {}".format(cell.posL, cell.posH, cell.data))
    print(asdict(dna))

if __name__ == '__main__':
    main()
