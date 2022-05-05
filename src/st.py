"""A balanced search tree."""

from __future__ import annotations
from dataclasses import (
    dataclass, field
)
from typing import (
    Protocol, TypeVar, Generic, Union,
    Optional,
    Any
)


# Some type stuff
class Ordered(Protocol):
    """Types that support < comparison."""

    def __lt__(self: Ord, other: Ord) -> bool:
        """Determine if self is < other."""
        ...


Ord = TypeVar('Ord', bound=Ordered)

# Tree structure


class EmptyClass(Generic[Ord]):
    """Empty tree."""

    # This is some magick to ensure we never have more
    # than one empty tree.
    _instance: Optional[EmptyClass[Any]] = None

    def __new__(cls) -> EmptyClass[Any]:
        """Create a new empty tree."""
        if cls._instance is None:
            cls._instance = super(EmptyClass, cls).__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        """Return 'Empty'."""
        return "Empty"

    @property
    def value(self) -> Ord:
        """Raise an exception."""
        raise AttributeError("No value on an empty tree")

    @property
    def height(self) -> int:
        """
        Return 0.

        The height of an empty tree is always 0.
        """
        return 0

    @property
    def left(self) -> Tree[Ord]:
        """Return an empty tree."""
        return Empty

    @property
    def right(self) -> Tree[Ord]:
        """Return an empty tree."""
        return Empty

    def __str__(self) -> str:
        """Return textual representation."""
        return "*"


# This is the one and only empty tree
Empty = EmptyClass()


@dataclass(frozen=True)
class InnerNode(Generic[Ord]):
    """
    Inner node in the search tree.

    Inner nodes are "frozen" to make them immutable. For this exercise, we want
    to work with persistent trees, so we cannot modify any existing tree, only
    make new trees that potentially share with existing trees.
    """

    value: Ord
    left: Tree[Ord] = Empty
    right: Tree[Ord] = Empty
    height: int = field(init=False)  # Don't set in init, fix in post_init.

    def __post_init__(self) -> None:
        """Fix consistency after creation."""
        object.__setattr__(
            self,
            'height', max(self.left.height, self.right.height) + 1
        )

    def __str__(self) -> str:
        """Return textual representation."""
        return f"({self.left}, {self.value}[{self.height}], {self.right})"


# A Tree is either an inner node or an empty tree
Tree = Union[InnerNode[Ord], EmptyClass]


def rot_left(n: Tree[Ord]) -> Tree[Ord]:
    """Rotate n left."""
    x, y = n.value, n.right.value
    a, b, c = n.left, n.right.left, n.right.right
    return InnerNode(y, InnerNode(x, a, b), c)


def rot_right(n: Tree[Ord]) -> Tree[Ord]:
    """Rotate n right."""
    x, y = n.value, n.left.value
    a, b, c = n.left.left, n.left.right, n.right
    return InnerNode(y, a, InnerNode(x, b, c))


def balance(n: Tree[Ord]) -> Tree[Ord]:
    """Return a balanced node for n."""
    if n.left.height < n.right.height - 1:
        return rot_left(n)
    if n.right.height < n.left.height - 1:
        return rot_right(n)
    return n


def contains(t: Tree[Ord], val: Ord) -> bool:
    """Test if val is in t."""
    while True:
        if t is Empty:
            return False
        if t.value == val:
            return True
        if val < t.value:
            t = t.left
        else:
            t = t.right


def insert(t: Tree[Ord], val: Ord) -> Tree[Ord]:
    """Insert val into t."""
    if t is Empty:
        return InnerNode(val, Empty, Empty)
    if t.value < val:
        return balance(InnerNode(t.value, t.left, insert(t.right, val)))
    if t.value > val:
        return balance(InnerNode(t.value, insert(t.left, val), t.right))
    return t


def rightmost(t: Tree[Ord]) -> Ord:
    """Get the rightmost value in t."""
    assert t is not Empty
    while t.right is not Empty:
        t = t.right
    return t.value


def remove(t: Tree[Ord], val: Ord) -> Tree[Ord]:
    """Remove val from t."""
    if t is Empty:
        return Empty

    if val < t.value:
        return balance(InnerNode(t.value, remove(t.left, val), t.right))
    if val > t.value:
        return balance(InnerNode(t.value, t.left, remove(t.right, val)))

    if t.left is Empty:
        return t.right
    if t.right is Empty:
        return t.left

    x = rightmost(t.left)
    return balance(InnerNode(x, remove(t.left, x), t.right))
