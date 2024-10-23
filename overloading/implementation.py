#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect

from .missing import _MISSING
from .datastructures import OverloadList
from .exceptions import NoMatchingOverload
from .type_matching import signature_matches


class Overload:
    def __set_name__(self, owner, name):
        self.owner = owner  # pylint: disable=attribute-defined-outside-init
        self.name = name  # pylint: disable=attribute-defined-outside-init

    def __init__(self, overload_list):
        if not isinstance(overload_list, OverloadList):
            raise TypeError('must use OverloadList')
        if not overload_list:
            raise ValueError('empty overload list')
        self.overload_list = overload_list
        self.signatures = [inspect.signature(f) for f, _ in overload_list]

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.overload_list!r})'

    def __get__(self, instance, _owner=None):
        if instance is None:
            return self
        # don't use owner == type(instance)
        # we want self.owner, which is the class from which get is being called
        return BoundOverloadDispatcher(instance, self.owner, self.name,
                                       self.overload_list, self.signatures)

    def __call__(self, *args, **kwargs):
        dispatcher = BoundOverloadDispatcher(self.owner, self.owner, self.name,
                                             self.overload_list, self.signatures)
        return dispatcher(*args, **kwargs)

    def extend(self, other):
        if not isinstance(other, Overload):
            raise TypeError
        self.overload_list.extend(other.overload_list)
        self.signatures.extend(other.signatures)


class BoundOverloadDispatcher:
    def __init__(self, instance, owner_cls, name, overload_list, signatures):
        self.instance = instance
        self.owner_cls = owner_cls
        self.name = name
        self.overload_list = overload_list
        self.signatures = signatures

    def best_match(self, *args, **kwargs):
        for (f, is_static), sig in zip(self.overload_list, self.signatures):
            try:
                if is_static:
                    bound_args = sig.bind(*args, **kwargs)
                else:
                    bound_args = sig.bind(self.instance, *args, **kwargs)
            except TypeError:
                pass  # missing/extra/unexpected args or kwargs
            else:
                bound_args.apply_defaults()
                # use the first one that matches
                if signature_matches(sig, bound_args):
                    return f, is_static

        raise NoMatchingOverload(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        try:
            f, is_static = self.best_match(*args, **kwargs)
        except NoMatchingOverload:
            pass
        else:
            if is_static:
                return f(*args, **kwargs)
            return f(self.instance, *args, **kwargs)

        # no matching overload in owner class, check next in line
        super_instance = super(self.owner_cls, self.instance)
        super_call = getattr(super_instance, self.name, _MISSING)
        if super_call is not _MISSING:
            return super_call(*args, **kwargs)
        raise NoMatchingOverload(*args, **kwargs)
