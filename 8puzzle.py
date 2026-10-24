
from collections import deque

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


def bfs(start):
    queue = deque([start])
    parent = {start: (None, None)}

    while queue:
        state = queue.popleft()

        if state == GOAL:
            path = []
            while parent[state][0] is not None:
                previous, move = parent[state]
                path.append(move)
                state = previous
            return path[::-1]

        for move, nxt in get_neighbors(state):
            if nxt not in parent:
                parent[nxt] = (state, move)
                queue.append(nxt)

    return None


def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join(
            str(x) if x != 0 else "_" for x in state[i:i + 3]
        ))
    print()


def main():
    print("Enter 9 numbers from 0 to 8 (0 = blank):")
    try:
        start = tuple(map(int, input().split()))
    except ValueError:
        print("Invalid input.")
        return

    if len(start) != 9 or sorted(start) != list(range(9)):
        print("Enter each number from 0 to 8 exactly once.")
        return

    if not is_solvable(start):
        print("This puzzle is not solvable.")
        return

    solution = bfs(start)

    if solution is None:
        print("No solution found.")
        return

    print("Solved in", len(solution), "moves.")
    print("Moves:", " -> ".join(solution) if solution else "None")

    state = start
    print("\nInitial state:")
    print_state(state)

    for step, move in enumerate(solution, 1):
        state = dict(get_neighbors(state))[move]
        print("Step", step, ":", move)
        print_state(state)


if __name__ == "__main__":
    main()
