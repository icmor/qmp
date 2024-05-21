# Quine-McCluskey Algorithm with Petrick's Method
This is an implementation of the Quine-McCluskey algorithm focused on simplicity and Pythonic idioms. The code eschews performance for didactic purposes, it uses sets and clean functions instead of lists and mutable state.

One may easily turn this more performant by actually creating a prime implicant table (instead of a function cache) and by using other techniques in conjunction with Petrick's method (like row/column domination).

## Requirements
Python 3.9 or greater is required. The program can be run directly from \_\_main\_\_.py but is meant to be run as a package. Just clone the repo and from the same directory run:
```bash
$ python -m qmp -h

usage: __main__.py [-h] [--dont-cares DC [DC ...]] MINTERMS [MINTERMS ...]

positional arguments:
  MINTERMS

options:
  -h, --help            show this help message and exit
  --dont-cares DC [DC ...], -dc DC [DC ...]
```

## Resources
* [Wikipedia QuineMcCluskey](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm)
* [Petrick's Method](https://www.allaboutcircuits.com/technical-articles/prime-implicant-simplification-using-petricks-method/)
* [Logic Optimization presentation](https://uweb.engr.arizona.edu/~ece474a/uploads/Main/lecture_logicopt2.pdf)

## Alternatives
* [Github Search Quine-McCluskey](https://github.com/topics/quine-mccluskey)
* [Espresso](https://github.com/Gigantua/Espresso)
