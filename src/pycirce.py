from collections.abc import Callable
from typing import Any, TypeVar

A = TypeVar("A")


class DecoderException(Exception):
    """An error representing any decoder failures"""


def decode_list(decoder: Callable[[Any], A]) -> Callable[[list[Any]], list[A]]:
    """Successively apply decoder over an entire array"""
    __name__ = f"decode_list({decoder.__name__})"  # pylint: disable=W0622

    def func(xs):
        try:
            return [decoder(x) for x in xs]
        except Exception as e:
            raise DecoderException(f"Error while applying {__name__}: {e}") from e

    func.__name__ = "decode_list({})".format(decoder.__name__)
    return func


def decode_object(decoder: Callable[..., A]) -> Callable[..., Callable[..., A]]:
    """
    @dataclass
    class Foo:
      bar: int
      baz: str

    decode_foo = decode_object(Foo)(bar=int)  # baz is not transformed,
    passed through as-is.

    decode_foo({'bar': '5', 'baz': 'blix'})  # Foo(bar=5, baz='blix')
    """

    def inner(**fields: Callable[[Any], Any]):
        __name__ = "decode_object({})".format(decoder.__name__)

        def func(obj: dict[str, Any]):
            try:
                return decoder(
                    **{k: fields[k](v) if k in fields else v for k, v in obj.items()}
                )
            except Exception as e:
                raise DecoderException(f"Error while applying {__name__}: {e}") from e

        func.__name__ = __name__
        return func

    __name__ = f"partially applied decode_object({decoder.__name__})"
    inner.__name__ = __name__
    inner.__qualname__ = __name__

    return inner
