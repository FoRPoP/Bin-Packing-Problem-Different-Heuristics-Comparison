from sortedcontainers import SortedList

from helpers import *

def next_fit(objects: list[float]) -> int:
    
    bins_count = 0
    curr_bin_space = 0
    for obj in objects:
        if curr_bin_space < obj:
            bins_count += 1
            curr_bin_space = 1
        curr_bin_space -= obj

    return bins_count


def next_k_fit(objects: list[float], k: int) -> int:
    
    open_bins = []
    for obj in objects:
        i = -min(k, len(open_bins))
        while i < 0:
            if open_bins[i] >= obj:
                open_bins[i] -= obj
                break
            i += 1
        if i == 0:
            open_bins.append(1.0 - obj)

    return len(open_bins)

def first_fit(objects: list[float]) -> int:
    
    node = construct_tree(len(objects))
    for obj in objects:
        node.pack(obj)
    
    return node.used_bins


def best_fit(objects: list[float]) -> int:

    bins = SortedList()
    for obj in objects:
        i = bins.bisect_left(obj)
        if i < len(bins):
            bins.add(bins.pop(i) - obj)
        else:
            bins.add(1.0 - obj)

    return len(bins)


def worst_fit(objects: list[float]) -> int:
    
    bins = SortedList()
    for obj in objects:
        if bins and bins[-1] >= obj:
            bins.add(bins.pop() - obj)
        else:
            bins.add(1.0 - obj)
    
    return len(bins)


def almost_worst_fit(objects: list[float]) -> int:
    
    bins = SortedList()
    for obj in objects:
        if len(bins) > 1 and bins[-2] >= obj:
            bins.add(bins.pop(-2) - obj)
        elif bins and bins[-1] >= obj:
            bins.add(bins.pop() - obj)
        else:
            bins.add(1.0 - obj)

    return len(bins)


def refined_first_fit(objects: list[float], offline: bool = False) -> int:
    
    counts = [len(objects)] * 4
    if offline:
        counts = count_objects_for_category(objects, [1/3, 2/5, 1/2, 1])

    categories_to_trees = {1: construct_tree(counts[0], 1/3), 2: construct_tree(counts[1], 2/5), 3: construct_tree(counts[2], 1/2), 4: construct_tree(counts[3], 1)}
    for obj in objects:
        tree = None
        if obj <= 1/3:
            tree = categories_to_trees[1]
        elif obj <= 2/5:
            tree = categories_to_trees[2]
        elif obj <= 1/2:
            tree = categories_to_trees[3]
        else:
            tree = categories_to_trees[4]
        tree.pack(obj)

    return sum(node.used_bins for node in categories_to_trees.values())


def harmonic_k(objects: list[float], k: int) -> int:
    
    bins_used = 0

    categories_to_bins = {1/i: 0 for i in reversed(range(1, k))}
    for obj in objects:
        for cat in categories_to_bins.keys():
            if obj <= cat:
                if obj > categories_to_bins[cat]:
                    categories_to_bins[cat] = 1.0 - obj
                    bins_used += 1
                else:
                    categories_to_bins[cat] -= obj
                break

    return bins_used

                
def refined_harmonic(objects: list[float], k: int) -> int:
    
    na = nb = nab = nbb = nbp = nc = 0
    bins_used = 0

    categories_to_bins = {}
    for i in reversed(range(1, k)):
        categories_to_bins[1/i] = 0

    for obj in objects:
        if obj > 1/2 and obj <= 59/95:
            if nb != 0:
                nb -= 1
                nab += 1
            else:
                na += 1
        elif obj > 1/3 and obj <= 37/96:
            if nbp == 1:
                nbp = 0
                nbb += 1
            elif nbb <= 3*nc:
                nbp = 1
            elif na != 0:
                na -= 1
                nab += 1
                nc += 1
            else:
                nb += 1
                nc += 1
        else:
            for cat in categories_to_bins.keys():
                if obj <= cat:
                    if obj > categories_to_bins[cat]:
                        categories_to_bins[cat] = 1.0 - obj
                        bins_used += 1
                    else:
                        categories_to_bins[cat] -= obj
                    break

    return na + nb + nab + nbb + nbp + bins_used
