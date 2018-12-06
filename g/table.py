import itertools


class SquareTable:
    def __init__(self, size: int, initializer=lambda x,y: None):
        self._table = {}
        self._size = size

        for x, y in self._xy_iterator():
            self[x, y] = initializer(x, y)

    @classmethod
    def filled_with(cls, size: int, entry):
        return cls(size, lambda x,y: entry)

    @classmethod
    def empty(cls, size: int):
        return cls.filled_with(size, None)

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
        for x in range(self._size):
            output += ", ".join(str(self[x, y]) for y in range(self._size)) + "\n"
        return output
