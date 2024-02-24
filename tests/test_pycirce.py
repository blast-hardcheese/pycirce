"""pycirce, a set of combinators for encoding and decoding data"""

import unittest

from dataclasses import dataclass
from pycirce import decode_list
from pycirce import decode_object


class DecodeListTestCase(unittest.TestCase):
    """Tests for decoding lists of things"""

    def test_decode_list(self):
        """Decode a list of integers"""
        decode_increment = decode_list(int)
        assert decode_increment(["1", "2", "3"]) == [1, 2, 3], "Should decode integers"


class DecodeObjectTestCase(unittest.TestCase):
    """Tests for decoding objects"""

    @dataclass
    class Person:
        """A simple dataclass to be decoded"""

        name: str
        age: int

    def test_decode_object(self):
        """Decode a single Person from a dict"""
        Person = DecodeObjectTestCase.Person

        decode_person = decode_object(Person)(age=int)
        decoded_person = decode_person({"name": "Alice", "age": "30"})
        assert decoded_person == Person(
            name="Alice", age=30
        ), "Age should be converted to int"

    def test_decode_list_of_persons(self):
        """Decode a list of Person"""
        Person = DecodeObjectTestCase.Person

        decode_list_of_persons = decode_list(decode_object(Person)(age=int))
        decoded_people = decode_list_of_persons(
            [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
        )
        assert decoded_people == [
            Person(name="Alice", age=30),
            Person(name="Bob", age=25),
        ], "Should decode a list of Person objects with ages converted to int"


if __name__ == "__main__":
    unittest.main()
