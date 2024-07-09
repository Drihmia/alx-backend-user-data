#!/usr/bin/env python3
""" This script tests the speed of checking the type of a variable using three different methods:
    1. type(red) != str
    2. type(red) is not str
    3. isinstance(red, str)
"""
import timeit


def test_type_check(iterations=1000000):
    """ This function tests the speed of checking the type of a variable """
    # Timing type(red) != str
    time_not_equal = timeit.timeit("type(red) != str", globals=globals(), number=iterations)

    # Timing type(red) is not str
    time_is_not = timeit.timeit("type(red) is not str", globals=globals(), number=iterations)

    # Timing isinstance(red, str)
    time_isinstance = timeit.timeit("not isinstance(red, str)", globals=globals(), number=iterations)

    print(time_not_equal, time_is_not, time_isinstance, end="\n\n")



if __name__ == "__main__":
    test = {
        "int": 123,
        "str": "123",
        "tuple": (1, 2, 3),
        "list": [1, 2, 3],
        "dict": {"a": 1, "b": 2, "c": 3}
    }

    for k, v in test.items():
        print(f"Testing for {k}")
        red = v
        print("time_not_equal------", "time_is_not---------", "time_isinstance")
        test_type_check()
