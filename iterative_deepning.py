
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVES = (
    ("Up", -1, 0),
    ("Down", 1, 0),
    ("Left", 0, -1),
    ("Right", 0, 1)
)

CUTOFF = "cutoff"


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


def depth_limited_search(state, limit, path, on_path, counter):
    counter[0] += 1

    if state == GOAL:
        return []

    if limit == 0:
        return CUTOFF

    cutoff_occurred = False

    for move, nxt in get_neighbors(state):
        if nxt in on_path:
            continue

        on_path.add(nxt)
        result = depth_limited_search(
            nxt, limit - 1, path, on_path, counter
        )
        on_path.remove(nxt)

        if result == CUTOFF:
            cutoff_occurred = True
        elif result is not None:
            return [move] + result

    return CUTOFF if cutoff_occurred else None


def iterative_deepening_search(start, max_depth=31):
    counter = [0]

    for limit in range(max_depth + 1):
        result = depth_limited_search(
            start, limit, [], {start}, counter
        )

        if result != CUTOFF:
            return result, counter[0]

    return None, counter[0]


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
        solution, nodes = iterative_deepening_search(start)

        if solution is None:
            print("No solution found within the depth limit.")
        else:
            print("Solution depth :", len(solution))
            print("Nodes visited  :", nodes)
            print("Moves          :", " -> ".join(solution)
                  if solution else "Already solved")
            print()
            print_solution(start, solution)
