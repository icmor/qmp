from .qmp import find_primes, get_min_primes
import argparse


def minterms_to_bin(minterms: set[int]) -> set[str]:
    maxlen = len(f"{max(minterms):b}")
    return {f"{m:0{maxlen}b}" for m in minterms}


def primes_to_minterms(primes: list[set[str]]) -> set[tuple[int, ...]]:
    return {tuple(sorted(int(m, 2) for m in prime)) for prime in primes}


def expand_primes(primes: set[str]) -> list[set[str]]:
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


parser = argparse.ArgumentParser()
parser.add_argument("minterms", metavar="MINTERMS", nargs="+", type=int)
args = parser.parse_args()

minterms = minterms_to_bin(args.minterms)
primes = get_min_primes(minterms, find_primes(minterms))
result = primes_to_minterms(expand_primes(primes))
print(result)
