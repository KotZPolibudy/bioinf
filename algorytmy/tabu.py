import random
from collections import namedtuple
from typing import List

Cell = namedtuple('Cell', ['posL', 'posH', 'data'])

class DNASequence:
    def __init__(self, length: int, start: str):
        self.sequence = start
        self.length = length

    def insert_cell(self, cell: Cell):
        overlap_length = min(cell.posH, self.length) - max(cell.posL, 0)
        if overlap_length > 0:
            overlap_start = max(cell.posL, 0)
            overlap_end = min(cell.posH, self.length)
            if overlap_start < len(self.sequence) and overlap_end >= 0:
                overlap_data = cell.data[max(0, -cell.posL): min(len(cell.data), self.length - cell.posL)]
                self.sequence = self.sequence[:overlap_start] + overlap_data + self.sequence[overlap_end:]

    def evaluate_fitness(self, target_sequence: str) -> int:
        fitness = 0
        for i in range(min(len(self.sequence), len(target_sequence))):
            if self.sequence[i] == target_sequence[i]:
                fitness += 1

        # Length-based fitness
        length_fitness = len(self.sequence)

        return fitness + length_fitness

def generate_neighbour(current_sequence: DNASequence, cells: List[Cell]) -> DNASequence:
    new_sequence = DNASequence(current_sequence.length, current_sequence.sequence)

    # Sort cells by their start position
    cells.sort(key=lambda x: x.posL)

    # Try different insertion points and combinations of cells
    for cell in cells:
        if cell.posH > len(new_sequence.sequence):
            overlap_start = max(0, len(new_sequence.sequence) - cell.posL)
            overlap_end = min(len(cell.data), current_sequence.length - len(new_sequence.sequence))
            if overlap_end > 0:
                new_sequence.sequence += cell.data[overlap_start: overlap_end]

    return new_sequence

def handle_gaps(current_sequence: DNASequence, cells: List[Cell]) -> DNASequence:
    # Identify gaps in the sequence
    gap_positions = [(i, i + 1) for i in range(len(current_sequence.sequence) - 1)
                     if current_sequence.sequence[i] == 'X' or current_sequence.sequence[i + 1] == 'X']
    for gap_start, gap_end in gap_positions:
        for cell in cells:
            if cell.posL <= gap_start and cell.posH >= gap_end:
                overlap_start = max(cell.posL, gap_start)
                overlap_end = min(cell.posH, gap_end)
                if overlap_end > overlap_start:
                    gap_data = cell.data[overlap_start - cell.posL: overlap_end - cell.posL]
                    current_sequence.sequence = current_sequence.sequence[:gap_start] + gap_data + current_sequence.sequence[gap_end:]
                    break
    return current_sequence

def taboo_search(initial_sequence: DNASequence, cells: List[Cell], target_sequence: str, max_iter: int = 1000,
                 tabu_size: int = 10) -> DNASequence:
    current_sequence = initial_sequence
    best_sequence = initial_sequence
    tabu_list = []

    for iteration in range(max_iter):
        neighbors = [generate_neighbour(current_sequence, cells) for _ in range(10)]
        neighbors = [handle_gaps(neighbor, cells) for neighbor in neighbors]
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

        # Print progress
        # print(f"Iteration {iteration + 1}: Best Fitness = {best_sequence.evaluate_fitness(target_sequence)}, Best Sequence = {best_sequence.sequence}")

    return best_sequence

def function_to_test(data):
    # Parameters for Tabu search
    ITERACJE = 1000
    ILE_ROZWIAZAN = 10
    start = data.start
    cells = data.cells
    target_length = data.length
    target_sequence = start.ljust(target_length, 'X')  # Pad the start sequence with 'X' to match the target length
    initial_sequence = DNASequence(target_length, start)
    reconstructed_sequence = taboo_search(initial_sequence, cells, target_sequence, ITERACJE, ILE_ROZWIAZAN)
    return reconstructed_sequence.sequence

# Integration into main function
if __name__ == '__main__':
    from parser import parse_xml

    filepath = "../data/4.xml"
    przyklad = parse_xml(filepath)

    res = function_to_test(przyklad)
    print(res)
