class Node:

    def __init__ (self, left: 'Node' = None, right: 'Node' = None, rem_space: float = 1.0) -> None:

        self.left = left
        self.right = right
        self.rem_space = rem_space
        self.used_bins = 0

    
    def pack (self, value: float) -> None:

        if not self.left and not self.right:
            if self.rem_space == 1.0:
                self.used_bins = 1
            self.rem_space -= value
            return
        
        if self.left.rem_space >= value:
            self.left.pack(value)
        else:
            self.right.pack(value)

        self.rem_space = max(self.left.rem_space, self.right.rem_space)
        self.used_bins = self.left.used_bins + self.right.used_bins


def construct_tree (leaves_amount: int, max_capacity: float = 1.0) -> Node:

    def build_tree (leaves_remaining: int):

        if leaves_remaining == 1:
            return Node(None, None, max_capacity)
        
        left_leaves = leaves_remaining // 2
        right_leaves = leaves_remaining - left_leaves

        left_subtree = build_tree(left_leaves)
        right_subtree = build_tree(right_leaves)

        return Node(left_subtree, right_subtree, max_capacity)

    if leaves_amount % 2 == 1:
        leaves_amount += 1

    if leaves_amount <= 0:
        return Node()
    
    return build_tree(leaves_amount)


def count_objects_for_category (objects: list[float], categories: list[float]) -> list[int]:

    counts = [0] * len(categories)
    for obj in objects:
        for i, cat in enumerate(categories):
            if obj <= cat:
                counts[i] += 1
                break

    return counts