
import heapq
from itertools import count

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


def misplaced_tiles(state, goal=GOAL):
    return sum(
        1 for i in range(9)
        if state[i] != 0 and state[i] != goal[i]
    )


def a_star(start, heuristic=manhattan_distance):
    tie = count()
    open_list = [
        (heuristic(start, GOAL), next(tie), 0, start)
    ]

    best_g = {start: 0}
    parent = {start: (None, None)}
    expanded = 0

    while open_list:
        f, _, g, state = heapq.heappop(open_list)

        if g != best_g.get(state):
            continue

        expanded += 1

        if state == GOAL:
            path = []
            while parent[state][0] is not None:
                previous, move = parent[state]
                path.append(move)
                state = previous

            return path[::-1], expanded

        for move, nxt in get_neighbors(state):
            new_g = g + 1

            if new_g < best_g.get(nxt, float("inf")):
                best_g[nxt] = new_g
                parent[nxt] = (state, move)

                new_f = new_g + heuristic(nxt, GOAL)
                heapq.heappush(
                    open_list,
                    (new_f, next(tie), new_g, nxt)
                )

    return None, expanded


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
        choice = input(
            "Heuristic [manhattan/misplaced] "
            "(default manhattan): "
        ).strip().lower()

        heuristic = (
            misplaced_tiles if choice == "misplaced"
            else manhattan_distance
        )

        solution, nodes = a_star(start, heuristic)

        if solution is None:
            print("No solution found.")
        else:
            print("Solution depth :", len(solution))
            print("Nodes expanded :", nodes)
            print("Moves          :", " -> ".join(solution)
                  if solution else "Already solved")
            print()
            print_solution(start, solution)
