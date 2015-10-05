__author__ = 'aman'
"""
Programming task
================

Implement the method iter_sample below to make the Unit test pass. iter_sample
is supposed to peek at the first n elements of an iterator, and determine the
minimum and maximum values (using their comparison operators) found in that
sample. To make it more interesting, the method is supposed to return an
iterator which will return the same exact elements that the original one would
have yielded, i.e. the first n elements can't be missing.

You may make use of Python's standard library. Python 3 is allowed, even though
it's not supported by codepad apparently.

Create your solution as a private fork, and send us the URL.
"""

from itertools import count
import unittest


def iter_sample(it, n):
    """
     Peek at the first n elements of an iterator, and determine the min and max
     values. Preserve all elements in the iterator!

     @param it: Iterator, potentially infinite
     @param n: Number of elements to peek off the iterator
     @return: Tuple of minimum, maximum (in sample), and an iterator that yields
     all elements that would have been yielded by the original iterator.
     """

    if n == 0:
        return None, None, None

    count = n
    iter_elements = []
    iter_elements.append(next(it))  # store elements from the iterator for later use
    min_val = iter_elements.index(0)  # set it to the first value
    max_val = iter_elements.index(0)  # set it to the first value
    for value in it:
        iter_elements.append(value)
        if min_val > value:
            min_val = value
        elif value > max_val:
            max_val = value
        count -= 1
        if count == 1:
            break
    it = (val for gen in (iter_elements, it) for val in gen)  # flattening of 2 lists helps us to maintain the iterator

    return min_val, max_val, it


class StreamSampleTestCase(unittest.TestCase):
    def test_smoke(self):
        # sample only the first 10 elements of a range of length 100

        it = iter(range(100))
        min_val, max_val, new_it = iter_sample(it, 10)

        self.assertEqual(0, min_val)
        self.assertEqual(9, max_val)
        # all elements are still there:
        self.assertEqual(list(range(100)), list(new_it))

    def test_sample_all(self):
        # sample more elements than there are - no error raised
        # now we now the global maximum!

        it = iter(range(100))
        min_val, max_val, new_it = iter_sample(it, 1000)

        self.assertEqual(0, min_val)
        self.assertEqual(99, max_val)
        self.assertEqual(list(range(100)), list(new_it))

    def test_infinite_stream(self):
        # and guess what - it also works with infinite iterators

        it = count(0)
        min_val, max_val, _ = iter_sample(it, 10)
	print min_val,max_val
        self.assertEqual(0, min_val)
        self.assertEqual(9, max_val)


if __name__ == "__main__":
    unittest.main()
