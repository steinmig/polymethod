#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Set, Tuple, Optional, Union, TypeVar, Iterable

from overloading import overload, OverloadMeta, NoMatchingOverload

T = TypeVar("T", List[int], Set[float])
X = 1


class A(metaclass=OverloadMeta):

    @staticmethod
    @overload
    def foo(x: int) -> int:
        return X + x

    @staticmethod
    @overload
    def foo(x: str) -> str:
        return str(X) + x

    @staticmethod
    @overload
    def foo(x: float) -> float:
        return X + x + 0.1

    @staticmethod
    @overload
    def foo(x: int, y: str) -> str:
        return str(X) + str(x) + y

    @staticmethod
    @overload
    def foo(x: Union[int, str], y: Union[int, str]) -> str:
        return str(X) + str(x) + str(y) + "!"

    @staticmethod
    @overload
    def foo(x: List[int]) -> int:
        return X + sum(x)

    @staticmethod
    @overload
    def foo(x: Dict[str, int]) -> int:
        return X + sum(x.values())

    @staticmethod
    @overload
    def foo(x: Set[int]) -> int:
        return X + sum(x) + 1

    @staticmethod
    @overload
    def foo(x: Tuple[int, int]) -> int:
        return X + sum(x) + 2

    @staticmethod
    @overload
    def foo(x: Optional[int]) -> int:
        if x is None:
            x = 0
        return X + x

    @staticmethod
    @overload
    def foo(x: Iterable[str]) -> float:
        return str(X) + ";".join(x)

    @staticmethod
    @overload
    def foo(x: T) -> int:
        return X + sum(x) + 0.1

    @staticmethod
    @overload
    def foo(x: Dict[Tuple[int, ...], List[int]]) -> int:
        return sum(sum(v) for v in x.values())

    @staticmethod
    @overload
    def foo(x) -> None:  # pylint: disable=unused-argument
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
