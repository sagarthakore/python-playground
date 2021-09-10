import unittest

def sort_items(arr):
    gt_dict = {}

    for item in arr:
        if '>' in item:
            item_vars = item.split('>')
            gt_dict[item_vars[0]] = item_vars[1]
        else:
            item_vars = item.split('<')
            gt_dict[item_vars[1]] = item_vars[0]

    current_var = list(set(gt_dict.keys()) - set(gt_dict.values()))[0]

    output = current_var

    while True:
        current_var = gt_dict.get(current_var)
        if current_var is None:
            break
        output += '>' + current_var

    return output


class TestStringMethods(unittest.TestCase):

    def test_sorter(self):
        self.assertEqual(sort_items(['B>A', 'C<A', 'D>B']), 'D>B>A>C')
        self.assertEqual(sort_items(['A>B', 'B>D', 'C<D']), 'A>B>D>C')
        self.assertEqual(sort_items(['C>B', 'D<B', 'A>C']), 'A>C>B>D')
        self.assertEqual(sort_items(['D>A', 'A>C', 'B<C']), 'D>A>C>B')
        self.assertEqual(sort_items(['B<A', 'C>A', 'D>C']), 'D>C>A>B')
        self.assertEqual(sort_items(['B>A', 'C<A', 'D>B']), 'D>B>A>C')


if __name__ == '__main__':
    print(sort_items(['B>A', 'C<A', 'D>B']))
    unittest.main()