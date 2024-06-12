import random
from collections import namedtuple
from typing import List

# Define the Cell namedtuple
Cell = namedtuple('Cell', ['posL', 'posH', 'data'])

# Define the DNASequence class to hold the sequence and operations related to it
class DNASequence:
    def __init__(self, length: int, start: str):
        self.sequence = start
        self.length = length

    def insert_cell(self, cell: Cell):
        """
        Inserts the data from the given cell into the sequence.
        """
        overlap_length = min(cell.posH, self.length) - max(cell.posL, 0)
        if overlap_length > 0:
            overlap_start = max(cell.posL, 0)
            overlap_end = min(cell.posH, self.length)
            if overlap_start < len(self.sequence) and overlap_end >= 0:
                overlap_data = cell.data[max(0, -cell.posL): min(len(cell.data), self.length - cell.posL)]
                self.sequence = self.sequence[:overlap_start] + overlap_data + self.sequence[overlap_end:]

    def evaluate_fitness(self, target_sequence: str) -> int:
        """
        Evaluate the fitness of the current sequence compared to the target sequence.
        """
        fitness = 0
        for i in range(min(len(self.sequence), len(target_sequence))):
            if self.sequence[i] == target_sequence[i]:
                fitness += 1
        return fitness

def generate_neighbour(current_sequence: DNASequence, cells: List[Cell]) -> DNASequence:
    """
    Generate a neighboring solution by randomly selecting a cell and inserting it into the sequence.
    """
    new_sequence = DNASequence(current_sequence.length, current_sequence.sequence)
    cell = random.choice(cells)
    new_sequence.insert_cell(cell)
    return new_sequence

def taboo_search(initial_sequence: DNASequence, cells: List[Cell], target_sequence: str, max_iter: int = 1000, tabu_size: int = 10) -> DNASequence:
    """
    Perform taboo search to reconstruct the DNA sequence from the given cells.
    """
    current_sequence = initial_sequence
    best_sequence = initial_sequence
    tabu_list = []

    for _ in range(max_iter):
        neighbors = [generate_neighbour(current_sequence, cells) for _ in range(10)]
        neighbors.sort(key=lambda x: -x.evaluate_fitness(target_sequence))

        best_neighbor = neighbors[0]
        if best_neighbor.evaluate_fitness(target_sequence) > best_sequence.evaluate_fitness(target_sequence):
            best_sequence = best_neighbor

        tabu_list.append(best_neighbor.sequence)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        current_sequence = best_neighbor
        if current_sequence.sequence in tabu_list:
            current_sequence = random.choice(neighbors)

    return best_sequence

def function_to_test(data):
    start = data.start
    cells = data.cells
    target_length = data.length
    target_sequence = start.ljust(target_length, 'X')  # Pad the start sequence with 'X' to match the target length
    initial_sequence = DNASequence(target_length, start)
    reconstructed_sequence = taboo_search(initial_sequence, cells, target_sequence)
    return reconstructed_sequence.sequence

# Integration into main function
if __name__ == '__main__':
    from parser import parse_xml

    filepath = "../data/4.xml"
    przyklad = parse_xml(filepath)

    res = function_to_test(przyklad)
    print(res)
