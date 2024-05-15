from collections import defaultdict
from itertools import combinations, product
from functools import reduce


def find_primes(minterms: set[str]) -> set[str]:
    def group_implicants() -> dict[int, set[str]]:
        groups = defaultdict(set)
        for minterm in minterms:
            groups[minterm.count('1')].add(minterm)
        return groups

    def differ_by_one(a: str, b: str) -> bool:
        return [c0 == c1 for c0, c1 in zip(a, b)].count(False) == 1

    def merge_implicants(a: str, b: str) -> str:
        return ''.join(c0 if c0 == c1 else '-' for c0, c1 in zip(a, b))

    groups = group_implicants()
    primes: set[str] = set()
    while True:
        new_implicants = defaultdict(set)
        non_primes = set()
        for i in range(max(groups.keys())):
            for a in groups[i]:
                for b in groups[i+1]:
                    if not differ_by_one(a, b):
                        continue
                    new_implicants[i].add(merge_implicants(a, b))
                    non_primes |= {a, b}
        primes = primes.union(*groups.values()) - non_primes
        if not new_implicants:
            return primes
        groups = new_implicants
