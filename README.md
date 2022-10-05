# pycle

Pycle is a light-weight and server-less interactive execution environment for Python.

It that works like jupyter notebook, but with out a long running server in the backend. After every execution, all the variables are stored in a file and loaded back for the next execution.
This approach makes it possible to work in environments with resource constraints and supports really long running sessions, without consuming additional resources.

## Command-line interface

Example 1:

```
$ python -m pycle -c 'x = 1'
$ python -m pycle -c 'y = 2'
$ python -m pycle -c 'x + y'
3
```

Example 2:

```
$ python -m pycle -c 'x = list(range(1000000))'
$ python -m pycle -c 'sum(x)'
499999500000
```

