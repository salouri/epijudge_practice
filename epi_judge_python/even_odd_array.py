import collections
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

# sort array so even numbers are first

def even_odd(A: List[int]) -> None:
    left, right = 0, len(A)-1
    while left < right:
        if isEven(A[left]):
            left += 1
        else:
            swap(A, left, right)
            right -= 1
    return A

def isEven(i: int)->bool:
    return True if i % 2 == 0 else False

def swap(a:list, l:int, r:int)->None:
    a[l], a[r] = a[r], a[l]

@enable_executor_hook
def even_odd_wrapper(executor, A):
    before = collections.Counter(A)

    executor.run(functools.partial(even_odd, A))

    in_odd = False
    for a in A:
        if a % 2 == 0:
            if in_odd:
                raise TestFailure('Even elements appear in odd part')
        else:
            in_odd = True
    after = collections.Counter(A)
    if before != after:
        raise TestFailure('Elements mismatch')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('even_odd_array.py',
                                       'even_odd_array.tsv', even_odd_wrapper))
