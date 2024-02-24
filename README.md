pycirce
===

[![Run on Repl.it](https://img.shields.io/badge/run-on_Replit-f26208?logo=replit)](https://repl.it/github/blast-hardcheese/pycirce) [![pypi: pycirce](https://img.shields.io/pypi/v/pycirce)](https://pypi.org/project/pycirce/)

Some primitive combinators for structurally decoding Python `dataclass`'s,
`namedtuple`'s, or other types.

Usage
---

## `pycirce.decode_list`

The `decode_list` combinator accepts a decoder as its first argument and returns a decoder:

```python
>>> decode_intlist = decode_list(int)
>>> decode_intlist(["1", "2", "3"])
[1, 2, 3]
```

## `pycirce.decode_object`

The `decode_object` combinator accepts a constructor as its first argument,
as well as a kwarg of parameter names to decoders for that particular name.

```python
>>> @dataclass
... class Person:
...     name: str
...     age: int
...
>>> decode_person = decode_object(Person)()
>>> decode_person({"name": "John Smith", "age": "45"})
Person(name='John Smith', age=45)
```

If members don't require downstream decoders, the second argument list kwargs can be
empty:

```python
>>> @dataclass
... class Person:
...     name: str
...     age: str
...
>>> decode_person = decode_object(Person)()
>>> decode_person({"name": "John Smith", "age": "45"})
Person(name='John Smith', age="45")
```
