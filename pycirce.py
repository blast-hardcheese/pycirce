from collections.abc import Callable
from typing import Any, TypeVar

A = TypeVar('A')


def decode_list(decoder: Callable[[Any], A]) -> Callable[[list[Any]], list[A]]:
  '''Successively apply decoder over an entire array'''

  def func(xs):
    return [decoder(x) for x in xs]

  func.__name__ = 'decode_list({})'.format(decoder.__name__)
  return func


def decode_object(
    decoder: Callable[..., A]) -> Callable[..., Callable[..., A]]:
  '''
  @dataclass
  class Foo:
    bar: int
    baz: str

  decode_foo = decode_object(Foo)(bar=int)  # baz is not transformed,
  passed through as-is.

  decode_foo({'bar': '5', 'baz': 'blix'})  # Foo(bar=5, baz='blix')
  '''

  def inner(**fields: Callable[[Any], Any]):
    __name__ = 'decode_object({})'.format(decoder.__name__)

    def func(obj: dict[str, Any]):
      try:
        return decoder(
            **{k: fields[k](v) if k in fields else v
               for k, v in obj.items()})
      except Exception as e:
        raise Exception('Error while applying {}: {}'.format(__name__, e))

    func.__name__ = __name__
    return func

  return inner
