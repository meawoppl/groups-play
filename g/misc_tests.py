import unittest

import g.misc

class MiscTests(unittest.TestCase):
    def test_pairs(self):
        pair_list = list(g.misc.pairs([1, 2, {}, 4]))
        self.assertEqual(len(pair_list), 3)
        
        self.assertEqual(pair_list[0], (1, 2))
        self.assertEqual(pair_list[1], (2, {}))
        self.assertEqual(pair_list[2], ({}, 4))
