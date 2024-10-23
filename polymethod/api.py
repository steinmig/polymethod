#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .datastructures import OverloadDict, OverloadList
from .implementation import Overload


def overload(f):
    f.__overload__ = True
    return f


class OverloadMeta(type):

    @classmethod
    def __prepare__(mcs, _name, _bases):
        return OverloadDict()

    def __new__(mcs, name, bases, namespace, **kwargs):
        overload_namespace = {
            key: Overload(val) if isinstance(val, OverloadList) else val
            for key, val in namespace.items()
        }
        return super().__new__(mcs, name, bases, overload_namespace, **kwargs)
