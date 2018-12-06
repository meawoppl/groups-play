import unittest

import g.table


class TableTests(unittest.TestCase):
    def test_sizes(self):
        pass
    
    def test_inits(self):
        t = g.table.SquareTable.empty(5)
        for element in t.get_flattened():
            self.assertEqual(element, None)
