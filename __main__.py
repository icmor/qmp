#!/usr/bin/env python
import argparse

if __package__ is None:
    from qmp import find_primes, get_min_primes		# type:ignore
else:
    from .qmp import find_primes, get_min_primes


def minterms_to_bin(minterms: set[int]) -> set[str]:
    """Turn a set of minterms given as numbers into their binary
    representation.
    """
    maxlen = len(f"{max(minterms):b}")
    return {f"{m:0{maxlen}b}" for m in minterms}


def primes_to_minterms(primes: list[set[str]]) -> set[tuple[int, ...]]:
    """Turn a list of prime implicants into their numeric representation."""
    return {tuple(sorted(int(m, 2) for m in prime)) for prime in primes}


def expand_primes(primes: set[str]) -> list[set[str]]:
    """Expand prime implicants into their covered minterms,
    eg. 1-1 -> 101, 111.
    """
    result = []
    for prime in primes:
        if "-" not in prime:
            result.append({prime})
            continue
        minterms = set()
        merged = [prime]
        while merged:
            current = merged.pop()
            a = current.replace("-", "0", 1)
            b = current.replace("-", "1", 1)
            if "-" in a:
                merged.append(a)
                merged.append(b)
            else:
                minterms |= {a, b}
        result.append(minterms)
    return result


parser = argparse.ArgumentParser(
    prog="qmp", description="Quine-McCluskey-Petrick minimization algorithm."
)
parser.add_argument("minterms", metavar="MINTERMS", nargs="+", type=int)
parser.add_argument("--dont-cares", "-dc", metavar="DC", nargs="+", type=int)
args = parser.parse_args()

minterms = minterms_to_bin(args.minterms)
if args.dont_cares:
    primes = find_primes(minterms | minterms_to_bin(args.dont_cares))
    primes = get_min_primes(minterms, primes, args.dont_cares)
else:
    primes = find_primes(minterms)
    primes = get_min_primes(minterms, primes)

result = primes_to_minterms(expand_primes(primes))
print(result)
