
import math
import random

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVES = (
    ("Up", -1, 0),
    ("Down", 1, 0),
    ("Left", 0, -1),
    ("Right", 0, 1)
)


def is_solvable(state):
    tiles = [x for x in state if x != 0]
    inversions = sum(
        tiles[i] > tiles[j]
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
    )
    return inversions % 2 == 0


def get_neighbors(state):
    blank = state.index(0)
    row, col = divmod(blank, 3)
    neighbors = []

    for name, dr, dc in MOVES:
        r, c = row + dr, col + dc

        if 0 <= r < 3 and 0 <= c < 3:
            pos = r * 3 + c
            new_state = list(state)
            new_state[blank], new_state[pos] = (
                new_state[pos], new_state[blank]
            )
            neighbors.append((name, tuple(new_state)))

    return neighbors


def manhattan_distance(state, goal=GOAL):
    goal_pos = {tile: i for i, tile in enumerate(goal)}
    distance = 0

    for i, tile in enumerate(state):
        if tile != 0:
            j = goal_pos[tile]
            distance += abs(i // 3 - j // 3)
            distance += abs(i % 3 - j % 3)

    return distance


def simulated_annealing(
    start, goal=GOAL, t_start=10.0,
    t_min=0.01, cooling_rate=0.995,
    steps_per_temp=50, max_steps=100000
):
    state = start
    path = []
    cost = manhattan_distance(state, goal)
    temperature = t_start
    steps = 0

    while temperature > t_min and cost > 0 and steps < max_steps:
        for _ in range(steps_per_temp):
            if steps >= max_steps or cost == 0:
                break

            move, candidate = random.choice(get_neighbors(state))
            new_cost = manhattan_distance(candidate, goal)
            delta = new_cost - cost
            steps += 1

            if delta < 0 or random.random() < math.exp(
                -delta / temperature
            ):
                state = candidate
                cost = new_cost
                path.append(move)

                if cost == 0:
                    return True, state, path, steps

        temperature *= cooling_rate

    return cost == 0, state, path, steps


def solve_with_restarts(start, goal=GOAL, max_restarts=50):
    total_steps = 0

    for attempt in range(1, max_restarts + 1):
        solved, state, path, steps = simulated_annealing(start, goal)
        total_steps += steps

        if solved:
            return path, attempt, total_steps

    return None, max_restarts, total_steps


def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join(
            str(x) if x != 0 else "_"
            for x in state[i:i + 3]
        ))
    print()


def print_solution(start, moves):
    state = start
    print("Initial state:")
    print_state(state)

    for step, move in enumerate(moves, 1):
        state = dict(get_neighbors(state))[move]
        print(f"Step {step}: {move}")
        print_state(state)


def get_start_state():
    text = input(
        "Enter 9 numbers from 0 to 8 (0 = blank): "
    )

    try:
        state = tuple(map(int, text.split()))
        if len(state) == 9 and sorted(state) == list(range(9)):
            return state
    except ValueError:
        pass

    print("Invalid input. Using default state.")
    return (1, 2, 3, 4, 0, 6, 7, 5, 8)


if __name__ == "__main__":
    start = get_start_state()

    if not is_solvable(start):
        print("This puzzle is not solvable.")
    else:
        solution, attempts, steps = solve_with_restarts(start)

        if solution is None:
            print(
                f"No solution found in {attempts} restarts "
                f"({steps} steps)."
            )
        else:
            print(f"Solved on attempt {attempts} ({steps} total steps).")
            print(f"Path length: {len(solution)} moves")
            print("Moves:", " -> ".join(solution)
                  if solution else "Already solved")
            print()
            print_solution(start, solution)
1