import itertools

from g.table import SquareTable
from g.group import Group

def solve_groups(g: Group):
    solver = g.get_solver()
    group_flat = g.get_flattened()

    # Create the decision builder.
    db = solver.Phase(
        group_flat,
        solver.CHOOSE_FIRST_UNBOUND,
        solver.ASSIGN_MIN_VALUE)

    # Create the solution collector.
    solution = solver.Assignment()
    solution.Add(group_flat)
    collector = solver.AllSolutionCollector(solution)

    print("Initiating solution for groups of order %i" % g.size())
    solver.Solve(db, [collector])
    print("Solutions found:", collector.SolutionCount())
    print("Time:", solver.WallTime(), "ms")
    print()

    return collector

def is_isomorphic(g1: Group, g2: Group):
    pass

def print_solution(coll, solution_number, group):
    get_xy_value = lambda x, y: to_symbols(coll.Value(solution_number, g[x, y]))
    print(SquareTable(group.size(), get_xy_value))

def print_title(title: str):
    print("*" * 20 + " " + title + " " + "*" * 20)

def to_symbols(val: int) -> str:
    if val == 1:
        return "1"
    return chr(ord("a") + val - 2)

group_size = 4
g = Group(group_size)
collector = solve_groups(g)

for solution_number in range(collector.SolutionCount()):
    print_title("Solution #%i" % solution_number)
    print()
    print_solution(collector, solution_number, g)
    print()