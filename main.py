import itertools
from ortools.constraint_solver import pywrapcp

class SquareTable:
    def __init__(self, size: int, initializer=lambda x,y: None):
        self._table = {}
        self._size = size

        for x, y in self._xy_iterator():
            self[x, y] = initializer(x, y)

    def _initial_table_entry(self, x, y):
        return None

    def _xy_iterator(self):
        return itertools.product(range(self._size), range(self._size))

    def get_trace(self):
        return tuple(self[i, i] for i in range(self._size))

    def get_row(self, row: int) -> tuple:
        self._assert_index(row)
        return tuple(self[row, col] for col in range(self._size))

    def get_col(self, col: int) -> tuple:
        self._assert_index(col)
        return tuple(self[row, col] for row in range(self._size))

    def _assert_index(self, index: int):
        assert (index >=0) and index < self._size

    def _validate_key(self, key):
        assert len(key) == 2, len(key)
        x, y = key
        self._assert_index(x)
        self._assert_index(y)
        return x, y

    def __getitem__(self, key):
        x, y = self._validate_key(key)
        return self._table[x, y]

    def __setitem__(self, key, item):
        x, y = self._validate_key(key)
        self._table[x, y] = item

    def get_flattened(self):
        return [self[x, y] for x, y in self._xy_iterator()]

    def size(self) -> int:
        return self._size

    def __str__(self):
        output = ""
        for x in range(group_size):
            output += ", ".join(str(self[x, y]) for y in range(group_size)) + "\n"
        return output

class Group(SquareTable):
    I = 1

    def __init__(self, size: int):
        self._s = pywrapcp.Solver("group_of_size_%i" % size)

        super().__init__(size, initializer=self._initial_table_entry)
        self._init_constraints()

    def _element_name(self, var: str, x: int, y: int) -> str:
        return self.__class__.__name__ + "." + var + "[%i,%i]" % (x, y)

    def _const_name(self, x: int, y: int) -> str:
        return self._element_name("Const", x, y)

    def _var_name(self, x: int, y: int) -> str:
        return self._element_name("Var", x, y)

    def _initial_table_entry(self, x, y):
        if (x == 0) and (y == 0):
            element = self._s.IntConst(self.I, self._const_name(x, y))
        elif (x == 0):
            element = self._s.IntConst(y + self.I, self._const_name(x, y))           
        elif (y == 0):
            element = self._s.IntConst(x + self.I, self._const_name(x, y))
        else:
            element = self._s.IntVar(self.I, self._size, self._var_name(x, y))
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
        for first, second in zip(trace_vars[:1], trace_vars[1:]):
            print(first, second)
            both_identity = (first == self.I) and (second == self.I)
            identity_first = (first == self.I) and (second != self.I)
            neither_identity = (first != self.I) and (second != self.I)
            self._s.Add(both_identity or identity_first or neither_identity) 

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


def print_solution(coll, solution_number, group):
    get_xy_value = lambda x, y: to_symbols(coll.Value(solution_number, g[x, y]))
    print(SquareTable(group.size(), get_xy_value))

def print_title(title: str):
    print("*" * 20 + " " + title + " " + "*" * 20)

def to_symbols(val: int) -> str:
    if val == 1:
        return "1"
    return chr(ord("a") + val - 2)

group_size = 8
g = Group(group_size)
collector = solve_groups(g)

for solution_number in range(collector.SolutionCount()):
    print_title("Solution #%i" % solution_number)
    print()
    print_solution(collector, solution_number, g)
    print()