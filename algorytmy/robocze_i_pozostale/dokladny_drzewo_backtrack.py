from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Cell:
    posL: int
    posH: int
    data: str


class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.cell: Optional[Cell] = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, cell: Cell):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.cell = cell

    def search_with_prefix(self, prefix: str) -> List[Cell]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_cells(node, prefix)

    def _collect_cells(self, node: TrieNode, prefix: str) -> List[Cell]:
        cells = []
        if node.cell:
            cells.append(node.cell)
        for char, child_node in node.children.items():
            cells.extend(self._collect_cells(child_node, prefix + char))
        return cells

    def delete_word(self, word: str):
        def _delete(node: TrieNode, word: str, depth: int) -> bool:
            if not node:
                return False
            if depth == len(word):
                if node.cell:
                    node.cell = None
                return len(node.children) == 0
            char = word[depth]
            if char in node.children and _delete(node.children[char], word, depth + 1):
                del node.children[char]
                return len(node.children) == 0 and node.cell is None
            return False

        _delete(self.root, word, 0)


def function_to_test(param):
    length = param.length
    start = param.start
    cells = param.cells
    n = len(start)
    trie = Trie()
    for cell in cells:
        trie.insert(cell.data, cell)

    # Delete the starting node from the trie
    trie.delete_word(start)

    dna_sequence = start
    sequence_stack = [(dna_sequence, cells.copy(), trie)]

    while sequence_stack:
        dna_sequence, current_cells, current_trie = sequence_stack.pop()

        if len(dna_sequence) >= length:
            return dna_sequence

        found = False
        for overlap in range(n - 1, 0, -1):
            prefix = dna_sequence[-overlap:]
            result = current_trie.search_with_prefix(prefix)
            if result:
                found = True
                for next_cell in result:
                    new_dna_sequence = dna_sequence + next_cell.data[overlap:]
                    new_trie = Trie()
                    for cell in current_cells:
                        if cell.data != next_cell.data:
                            new_trie.insert(cell.data, cell)
                    sequence_stack.append(
                        (new_dna_sequence, [cell for cell in current_cells if cell.data != next_cell.data], new_trie))
                break

        if not found and len(dna_sequence) < length:
            continue  # No progress can be made, backtrack to try another path

    return dna_sequence  # If no sequence meets the required length, return the best attempt


if __name__ == '__main__':
    from parser import parse_xml

    filepath = "../../data/4.xml"
    przyklad = parse_xml(filepath)

    res = function_to_test(przyklad)
    print(res)