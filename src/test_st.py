"""Testing search tree balancing."""

import random
from st import (
    Tree, Empty,
    insert, remove, contains
)


def test_tree() -> None:
    """Test that we still have a working search tree."""
    x: list[int] = random.sample(range(0, 10), 5)
    t: Tree[int] = Empty
    for i, a in enumerate(x):
        t = insert(t, a)
        for b in x[:i+1]:
            assert contains(t, b)
    for i, a in enumerate(x):
        t = remove(t, a)
        for b in x[:i+1]:
            assert not contains(t, b)
    assert t is Empty
