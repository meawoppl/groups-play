import itertools
from ortools.constraint_solver import pywrapcp

from g.table import SquareTable


class Group(SquareTable):
    I = 1

    def __init__(self, size: int):
        self._s = pywrapcp.Solver("group_of_size_%i" % size)

        super().__init__(size, initializer=self._initial_table_entry)
        self._init_constraints()

    def _name(self, var: str, x: int, y: int) -> str:
        return self.__class__.__name__ + "." + var + "[%i,%i]" % (x, y)

    def _initial_table_entry(self, x, y):
        if (x == 0):
            element = self._s.IntConst(y + self.I, self._name("Const", x, y))           
        elif (y == 0):
            element = self._s.IntConst(x + self.I, self._name("Const", x, y))
        else:
            element = self._s.IntVar(self.I, self._size, self._name("Var", x, y))
        return element

    def _init_constraints(self):
        # Entries per row must be unique
        for x in range(self._size):
            row = self.get_row(x)
            self._s.Add(self._s.AllDifferent(row))

        # Entries per col must be unique
        for y in range(self._size):
            col = self.get_col(y)
            self._s.Add(self._s.AllDifferent(col))

        # Ones lead constraint
        trace_vars = self.get_trace()
        for first, second in zip(trace_vars[:-1], trace_vars[1:]):
            both_identity = (first == self.I) and (second == self.I)
            identity_first = (first == self.I) and (second != self.I)
            neither_identity = (first != self.I) and (second != self.I)
            self._s.Add(both_identity or identity_first or neither_identity) 

        for i, trace_var in enumerate(trace_vars[:-1]):
            trace_element_ident = trace_var == self.I
            permutation_on_adjacent = (self[i, i+1] == self.I) and (self[i+1,i] == self.I)
            self._s.Add(trace_element_ident or permutation_on_adjacent)

    def get_solver(self):
        return self._s


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