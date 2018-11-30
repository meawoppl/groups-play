import itertools
from ortools.constraint_solver import pywrapcp

class Group:
    def __init__(self, size: int, solver):
        self._size = size
        self._table = {}
        self._s = solver
        self._init_table()

    def _xy_iterator(self):
        return itertools.product(range(self._size), range(self._size))

    def _element_name(self, var: str, x: int, y: int) -> str:
        return self.__class__.__name__ + "." + var + "[%i,%i]" % (x, y)

    def _const_name(self, x: int, y: int) -> str:
        return self._element_name("Const", x, y)

    def _var_name(self, x: int, y: int) -> str:
        return self._element_name("Var", x, y)

    def _init_table(self):
        for x, y in self._xy_iterator():
            if (x == 0) and (y == 0):
                element = self._s.IntConst(1, self._const_name(x, y))
            elif (x == 0):
                element = self._s.IntConst(y + 1, self._const_name(x, y))           
            elif (y == 0):
                element = self._s.IntConst(x + 1, self._const_name(x, y))
            else:
                element = self._s.IntVar(1, self._size, self._var_name(x, y))
            self[x, y] = element

        for x in range(self._size):
            row = [self[x, y] for y in range(self._size)]
            self._s.Add(self._s.AllDifferent(row))

        for y in range(self._size):
            col = [self[x, y] for x in range(self._size)]
            self._s.Add(self._s.AllDifferent(col))

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


solver = pywrapcp.Solver("find_groups")

group_size = 6
g = Group(group_size, solver)

group_flat = g.get_flattened()

# Create the decision builder.
db = solver.Phase(group_flat, solver.CHOOSE_FIRST_UNBOUND,
                solver.ASSIGN_MIN_VALUE)

# Create the solution collector.
solution = solver.Assignment()
solution.Add(group_flat)
collector = solver.AllSolutionCollector(solution)

solver.Solve(db, [collector])
print("Solutions found:", collector.SolutionCount())
print("Time:", solver.WallTime(), "ms")
print()

def print_title(title: str):
    print("*" * 20 + " " + title + " " + "*" * 20)

def to_symbols(val: int) -> str:
    if val == 1:
        return "1"
    return chr(ord("a") + val - 2)

for solution_number in range(collector.SolutionCount()):
    print_title("Solution #%i" % solution_number)
    for x in range(group_size):
        print("  " + ", ".join(to_symbols(collector.Value(solution_number, g[x, y])) for y in range(group_size))
        )
