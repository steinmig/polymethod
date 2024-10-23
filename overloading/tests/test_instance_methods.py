#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Set, Tuple, Optional, Union, TypeVar, Iterable

from overloading import overload, OverloadMeta, NoMatchingOverload

T = TypeVar("T", List[int], Set[float])


class A(metaclass=OverloadMeta):

    def __init__(self, x: int) -> None:
        self.x = x

    @overload
    def foo(self, x: int) -> int:
        return self.x + x

    @overload
    def foo(self, x: str) -> str:
        return str(self.x) + x

    @overload
    def foo(self, x: float) -> float:
        return self.x + x + 0.1

    @overload
    def foo(self, x: int, y: str) -> str:
        return str(self.x) + str(x) + y

    @overload
    def foo(self, x: Union[int, str], y: Union[int, str]) -> str:
        return str(self.x) + str(x) + str(y) + "!"

    @overload
    def foo(self, x: List[int]) -> int:
        return self.x + sum(x)

    @overload
    def foo(self, x: Dict[str, int]) -> int:
        return self.x + sum(x.values())

    @overload
    def foo(self, x: Set[int]) -> int:
        return self.x + sum(x) + 1

    @overload
    def foo(self, x: Tuple[int, int]) -> int:
        return self.x + sum(x) + 2

    @overload
    def foo(self, x: Optional[int]) -> int:
        if x is None:
            x = 0
        return self.foo(x)

    @overload
    def foo(self, x: Iterable[str]) -> float:
        return str(self.x) + ";".join(x)

    @overload
    def foo(self, x: T) -> int:
        return self.x + sum(x) + 0.1

    @overload
    def foo(self, x: Dict[Tuple[int, ...], List[int]]) -> int:
        return sum(sum(v) for v in x.values())

    @overload
    def foo(self, x) -> None:  # pylint: disable=unused-argument
        return None


def test_overloads():
    a = A(1)
    assert a.foo(1) == 2
    assert a.foo("1") == "11"
    assert a.foo(1.0) == 2.1
    assert a.foo(1, "2") == "112"
    assert a.foo(1, 2) == "112!"
    assert a.foo([1, 2, 3]) == 7
    assert a.foo({"a": 1, "b": 2, "c": 3}) == 7
    assert a.foo({1, 2, 3}) == 8
    assert a.foo((1, 2)) == 1 + 3 + 2
    assert a.foo(None) == 1
    assert a.foo(["a", "b", "c"]) == "1a;b;c"
    assert a.foo([1, 2, 3]) == 7
    assert a.foo({(1, 2): [1, 2, 3], (4, 5): [4, 5, 6]}) == 21
    assert a.foo(object) is None
    try:
        a.foo(1, 2, 3)
    except NoMatchingOverload:
        pass
    else:
        assert False, "NoMatchingOverload not raised"
    try:
        a.foo(1, 2, 3, 4)
    except NoMatchingOverload:
        pass
    else:
        assert False, "NoMatchingOverload not raised"
    try:
        a.foo(1, 2.1)
    except NoMatchingOverload:
        pass
    else:
        assert False, "NoMatchingOverload not raised"
