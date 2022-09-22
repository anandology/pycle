# pycle

Pycle is a light-weight and server-less interactive execution environment for Python.

It that works like jupyter notebook, but with out a long running server in the backend. After every execution, all the variables are stored in to a database and retried for the next execution.
This approach makes it possible to work in environments with resource constraints and supports really long running sessions, without consuming additional resources.

## Command-line interface

```
$ pycle -c 'x = 1'
$ pycle -c 'print(x)'
1
```

