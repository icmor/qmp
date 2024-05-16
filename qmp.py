from collections import defaultdict
from functools import lru_cache, reduce
from itertools import permutations
from string import ascii_letters


def find_primes(minterms: set[str]) -> set[str]:
    """Find all prime implicants by combining a set of minterms."""
    def group_implicants() -> dict[int, set[str]]:
        """Divide implicants into groups based on the number of 1's."""
        groups = defaultdict(set)
        for minterm in minterms:
            groups[minterm.count('1')].add(minterm)
        return groups

    def differ_by_one(a: str, b: str) -> bool:
        """Check if two minterms differ by a single character."""
        return [c0 == c1 for c0, c1 in zip(a, b)].count(False) == 1

    def merge_implicants(a: str, b: str) -> str:
        """Return the prime implicant that covers both implicants."""
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


def get_min_primes(minterms: set[str], primes: set[str],
                   dc: set[str] | None = None) -> set[str]:
    """Get the minimum possible prime implicants to cover all minterms
    provided. First the function finds all essential primes and if they
    don't create a full cover it then uses Petrick's method to find an
    optimal solution.
    """
    @lru_cache(maxsize=len(minterms) * len(primes))
    def covers(prime: str, minterm: str) -> bool:
        """Check if a prime implicant covers a minterm."""
        return all(p == '-' or p == m for p, m in zip(prime, minterm))

    def distribute(a: set[str], b: set[str]) -> set[str]:
        """Apply the distributive law to distribute a sum over a product."""
        result = set()
        for x in a:
            for y in b:
                result.add(''.join(sorted(set(x + y))))
        return result

    def absorption(sop: set[str]) -> set[str]:
        """Apply the absorption law repeatedly until no further
        simplification is possible.
        """
        sop = sop.copy()
        while True:
            for a, b in permutations(sop, 2):
                if all(c in b for c in a):
                    sop.discard(b)
                    break
            else:
                return sop

    # Remove primes that only cover don't cares
    if dc:
        primes = primes - {p for p in primes
                           if all(m in dc for m in minterms if covers(p, m))}
    # Find essential primes
    essential = set()
    for minterm in minterms:
        filtered = [p for p in primes if covers(p, minterm)]
        if len(filtered) == 1:
            essential.add(filtered[0])
    minterms = (minterms
                - {m for p in essential for m in minterms if covers(p, m)})
    if not minterms:
        return essential

    primes = primes - essential
    if len(primes) > len(ascii_letters):
        print("Too many prime implicants left.")
        return primes | essential

    # Petrick's method
    prime_dict = {p: letter for p, letter in zip(primes, ascii_letters)}
    pos = [{prime_dict[p] for p in primes if covers(p, m)} for m in minterms]
    sop = absorption(reduce(distribute, pos))
    smallest = min(sop, key=len)
    return essential | {k for k, v in prime_dict.items() if v in smallest}
