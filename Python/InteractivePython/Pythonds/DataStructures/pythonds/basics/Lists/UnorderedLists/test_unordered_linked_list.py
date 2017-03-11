from unittest import TestCase
from random import randint

from unordered_linked_list import UnorderedList


class UnorderedLinkedListTest(TestCase):

    def get_data(self, linked_list):
        current = linked_list.head
        data = []
        while current and current.get_next():
            data.append(current.get_data())
            current = current.get_next()
        if current:
            data.append(current.get_data())
        return data

    def test_is_empty(self):
        L = UnorderedList()
        self.assertTrue(L.is_empty())
        L.add(32)
        self.assertFalse(L.is_empty())

    def test_add(self):
        data = [randint(0, 100) for i in range(10)]
        L = UnorderedList()
        for d in data:
            L.add(d)
        self.assertFalse(L.is_empty())
        self.assertEqual(sorted(data), sorted(self.get_data(L)))

    def test_size(self):
        L = UnorderedList()
        for i in range(10):
            L.add(i)
        self.assertEqual(L.size(), 10)

    def test_search(self):
        L = UnorderedList()
        data = [randint(0, 100) for i in range(10)]
        for d in data:
            L.add(d)
        self.assertTrue(all([L.search(i) for i in data]))
        self.assertFalse(all([L.search(i) for i in range(100, 110)]))

    def test_remove(self):
        L = UnorderedList()
        data = [1, 2, 3, 4, 5]
        for d in data:
            L.add(d)
        L.remove(3)
        self.assertNotIn(3, self.get_data(L))
        L.remove(5)
        self.assertNotIn(5, self.get_data(L))

    def test_remove_with_one_element(self):
        L = UnorderedList()
        L.add(3)
        L.remove(3)
        self.assertNotIn(3, self.get_data(L))
        self.assertEqual(L.size(), 0)

    def test_append(self):
        pass

    def test_insert(self):
        pass

    def test_index(self):
        pass

    def test_pop(self):
        pass
