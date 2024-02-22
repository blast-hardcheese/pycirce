from pycirce import decode_list
from pycirce import decode_object
from dataclasses import dataclass


def test_decode_list():
  decode_increment = decode_list(int)
  assert decode_increment(['1', '2', '3']) == [1, 2,
                                               3], "Should decode integers"


@dataclass
class Person:
  name: str
  age: int


def test_decode_object():
  decode_person = decode_object(Person)(age=int)
  decoded_person = decode_person({'name': 'Alice', 'age': '30'})
  assert decoded_person == Person(name='Alice',
                                  age=30), "Age should be converted to int"


def test_decode_list_of_persons():
  decode_list_of_persons = decode_list(decode_object(Person)(age=int))
  decoded_people = decode_list_of_persons([
      {'name': 'Alice', 'age': '30'},
      {'name': 'Bob', 'age': '25'}
  ])
  assert decoded_people == [
      Person(name='Alice', age=30),
      Person(name='Bob', age=25)
  ], "Should decode a list of Person objects with ages converted to int"