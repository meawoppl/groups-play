import unittest

import g.table


class TableTests(unittest.TestCase):
    def test_sizes(self):
        pass
    
    def test_inits(self):
        t = g.table.SquareTable.empty(5)
        for element in t.get_flattened():
            self.assertEqual(element, None)

    def test_getters(self):
        t = g.table.SquareTable(5, lambda row,col: col)
        
        self.assertEqual(t.get_row(3), (0, 1, 2, 3, 4))
        self.assertEqual(t.get_col(4), (4, 4, 4, 4, 4))

        self.assertEqual(t.get_trace(), (0, 1, 2, 3, 4))

    def test_get_size(self):
        for i in range(2, 7):
            t = g.table.SquareTable(i, lambda row,col: col)
            self.assertEqual(t.size(), i)

    def test_stringify(self):
        # We don't really enforce the format, just that it works
        t = g.table.SquareTable(6, lambda row,col: col)
        self.assertGreater(len(str(t)), 0)
