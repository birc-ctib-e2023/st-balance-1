# Balancing search trees -- 1

The trick to getting `O(log n)` operations on a binary search tree is to keep the tree balanced, which means that from the root to any leaf, you have the same length. This strict level of ballanced is rarely possible, you can only achieve it if `n` is a power of two, but the best you can achive is that for any node, the longest path to a leaf in one sub-tree is at most one longer than the longest path to a leaf in the other sub-tree.

Even this, though, is rarely achievable, and we have to make do with even looser definitions of balanced. [Red-black trees](https://en.wikipedia.org/wiki/Red–black_tree), for example, guarantees the difference between the longest and the shortest path to a leaf is at most a factor two. Luckily, that also suffices to get logarithmic height.

The way to balance trees is often a local transformation of sub-trees. When inserting or removing elements we transform the tree by locally moving sub-trees around. In the book, you can see the transformations that red-black trees use. For persistent trees the overhead is in `O(log n)`, so within the time we need to spend on modifying the tree anyway, and for ephemeral trees we can do the transformations in `O(1)` amortised.

We won't attempt implementing the red-black transformations in this exercise, and we won't actually achieve balanced trees either, but we will see how we can implement the kind of transformations used in other techniques. What we will do is, when we see a sub-tree that isn't balanced, we will try to lift up the tree with the highest height, getting it closer to the root, at the cost of the tree with the lower height, that won't suffer so much from moving further down in the tree. We do this with one of two operations, that we will call *rotations*. (That is also what it is called with more sophisticated methods, so I didn't just make the word up).

