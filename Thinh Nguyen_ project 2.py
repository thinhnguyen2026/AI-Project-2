class PuzzleState:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth

    def generate_moves(self):
        moves = []
        zero_pos = self.state.index(0)
        if zero_pos % 3 != 0:  # Can move left
            moves.append('Left ')
        if zero_pos % 3 != 2:  # Can move right
            moves.append('Right ')
        if zero_pos > 2:  # Can move up
            moves.append('Up ')
        if zero_pos < 6:  # Can move down
            moves.append('Down ')
        return moves

    def execute_move(self, move):
        zero_pos = self.state.index(0)
        new_state = list(self.state)
        if move == 'Left ':
            swap_pos = zero_pos - 1
        elif move == 'Right ':
            swap_pos = zero_pos + 1
        elif move == 'Up ':
            swap_pos = zero_pos - 3
        elif move == 'Down ':
            swap_pos = zero_pos + 3
        new_state[zero_pos], new_state[swap_pos] = new_state[swap_pos], new_state[zero_pos]
        return PuzzleState(new_state, self, move, self.depth + 1)

    def manhattan_distance(self):
        distance = 0
        for i in range(9):
            if self.state[i] == 0: continue  # Skip the empty tile
            x, y = divmod(i, 3)
            goal_x, goal_y = divmod(self.state[i] - 1, 3)
            distance += abs(x - goal_x) + abs(y - goal_y)
        return distance

    def is_goal(self):
        # Assuming goal state is [1, 2, 3, 8, 0, 4, 7, 6, 5]
        return self.state == [1, 2, 3, 8, 0, 4, 7, 6, 5]

    
import heapq

def a_star_solve(start_state):
    start = PuzzleState(start_state)
    priority_queue = []
    counter = 0  # Unique identifier for each entry
    heapq.heappush(priority_queue, (start.manhattan_distance(), counter, start))
    visited = set()
    nodes_expanded = 0

    while priority_queue:
        _, _, current = heapq.heappop(priority_queue)
        if tuple(current.state) in visited:
            continue
        visited.add(tuple(current.state))
        nodes_expanded += 1

        if current.is_goal():
            return current, current.depth, nodes_expanded

        for move in current.generate_moves():
            next_state = current.execute_move(move)
            if tuple(next_state.state) in visited:
                continue
            counter += 1  # Increment the counter for each new state
            heapq.heappush(priority_queue, (next_state.depth + next_state.manhattan_distance(), counter, next_state))

    return None, None, nodes_expanded



from collections import deque

def bfs_solve(start_state):
    start = PuzzleState(start_state)
    if start.state == [1, 2, 3, 8, 0, 4, 7, 6, 5]:
        return start, 0, 0  # Already solved
    
    queue = deque([start])
    visited = set()
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        visited.add(tuple(current.state))
        nodes_expanded += 1

        for move in current.generate_moves():
            next_state = current.execute_move(move)
            if tuple(next_state.state) in visited:
                continue
            if next_state.state == [1, 2, 3, 8, 0, 4, 7, 6, 5]:
                return next_state, next_state.depth, nodes_expanded
            queue.append(next_state)

    return None, None, nodes_expanded

def print_solution(solution_state):
    path = []
    current = solution_state
    while current.parent is not None:
        path.append(current.move)
        current = current.parent
    path.reverse()
    return path

def read_puzzle_from_file(filename):
    try:
        with open(filename, 'r') as file:
            puzzle = [list(map(int, line.split())) for line in file]
        return puzzle
    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")
        return None
    
def print_initial_puzzle_state(puzzle):
    if puzzle is not None:
        print("Initial state of the puzzle:")
        for row in puzzle:
            print(' '.join(map(str, row)))    

def main():
    print("Welcome to the Eight-Puzzle Solver!")
    print("In this game you will need to input your file of puzzle that involves sliding tiles on a 3x3 grid containing 8 tiles and an empty spot.")
    print("And then, I will determine the path from a given starting state to the goal, as well as how many nodes were expanded during the search.")
    print("Now let's start it")
    filename = input("Enter the filename of the puzzle you want to solve: ")
    puzzle = read_puzzle_from_file(filename)
    
    if puzzle is None:
        return  # Exit if the puzzle couldn't be loaded
    
    flattened_puzzle = [tile for row in puzzle for tile in row]
    print_initial_puzzle_state(puzzle)

    choice = input("Choose the algorithm: 1 for BFS, 2 for A*: ")
    if choice == '1':
        solution_state, solution_depth, nodes_expanded = bfs_solve(flattened_puzzle)
    elif choice == '2':
        solution_state, solution_depth, nodes_expanded = a_star_solve(flattened_puzzle)
    else:
        print("Invalid choice.")
        return

    if solution_state:
        path = print_solution(solution_state)
        print("Solution path:", ''.join(path))
        print("Number of moves:", solution_depth)
        print("Total nodes expanded:", nodes_expanded)
    else:
        print("No solution found.")
  
if __name__ == "__main__":
    main()
