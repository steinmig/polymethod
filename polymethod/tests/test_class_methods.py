#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Set, Tuple, Optional, Union, TypeVar, Iterable

from polymethod import overload, OverloadMeta, NoMatchingOverload

T = TypeVar("T", List[int], Set[float])


class A(metaclass=OverloadMeta):

    x = 1

    @classmethod
    @overload
    def foo(cls, x: int) -> int:
        return cls.x + x

    @classmethod
    @overload
    def foo(cls, x: str) -> str:
        return str(cls.x) + x

    @classmethod
    @overload
    def foo(cls, x: float) -> float:
        return cls.x + x + 0.1

    @classmethod
    @overload
    def foo(cls, x: int, y: str) -> str:
        return str(cls.x) + str(x) + y

    @classmethod
    @overload
    def foo(cls, x: Union[int, str], y: Union[int, str]) -> str:
        return str(cls.x) + str(x) + str(y) + "!"

    @classmethod
    @overload
    def foo(cls, x: List[int]) -> int:
        return cls.x + sum(x)

    @classmethod
    @overload
    def foo(cls, x: Dict[str, int]) -> int:
        return cls.x + sum(x.values())

    @classmethod
    @overload
    def foo(cls, x: Set[int]) -> int:
        return cls.x + sum(x) + 1

    @classmethod
    @overload
    def foo(cls, x: Tuple[int, int]) -> int:
        return cls.x + sum(x) + 2

    @classmethod
    @overload
    def foo(cls, x: Optional[int]) -> int:
        if x is None:
            x = 0
        return cls.foo(x)

    @classmethod
    @overload
    def foo(cls, x: Iterable[str]) -> float:
        return str(cls.x) + ";".join(x)

    @classmethod
    @overload
    def foo(cls, x: T) -> int:
        return cls.x + sum(x) + 0.1

    @classmethod
    @overload
    def foo(cls, x: Dict[Tuple[int, ...], List[int]]) -> int:
        return sum(sum(v) for v in x.values())

    @classmethod
    @overload
    def foo(cls, x) -> None:  # pylint: disable=unused-argument
        return None


def test_overloads_classmethod():
    assert A.foo(1) == 2
    assert A.foo("1") == "11"
    assert A.foo(1.0) == 2.1
    assert A.foo(1, "2") == "112"
    assert A.foo(1, 2) == "112!"
    assert A.foo([1, 2, 3]) == 7
    assert A.foo({"a": 1, "b": 2, "c": 3}) == 7
    assert A.foo({1, 2, 3}) == 8
    assert A.foo((1, 2)) == 1 + 3 + 2
    assert A.foo(None) == 1
    assert A.foo(["a", "b", "c"]) == "1a;b;c"
    assert A.foo([1, 2, 3]) == 7
    assert A.foo({(1, 2): [1, 2, 3], (4, 5): [4, 5, 6]}) == 21
    assert A.foo(object) is None
    try:
        A.foo(1, 2, 3)
    except NoMatchingOverload:
        pass
    else:
        assert False, "NoMatchingOverload not raised"
    try:
        A.foo(1, 2, 3, 4)
    except NoMatchingOverload:
        pass
    else:
        assert False, "NoMatchingOverload not raised"
    try:
        A.foo(1, 2.1)
    except NoMatchingOverload:
        pass
    else:
        assert False, "NoMatchingOverload not raised"
