#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .missing import _MISSING


class OverloadList(list):
    pass


class OverloadDict(dict):

    def __setitem__(self, key, value):
        assert isinstance(key, str), 'keys must be str'

        prior_val = self.get(key, _MISSING)

        is_static = isinstance(value, staticmethod)
        if is_static or isinstance(value, classmethod):
            overloaded = getattr(getattr(value, '__func__'), '__overload__', False)
            if overloaded:
                value = getattr(value, '__func__')
        else:
            overloaded = getattr(value, '__overload__', False)

        if prior_val is _MISSING:
            insert_val = OverloadList([(value, is_static)]) if overloaded else value
            super().__setitem__(key, insert_val)
        elif isinstance(prior_val, OverloadList):
            if not overloaded:
                raise ValueError(self._errmsg(key))
            prior_val.append((value, is_static))
        else:
            if overloaded:
                raise ValueError(self._errmsg(key))
            super().__setitem__(key, value)

    @staticmethod
    def _errmsg(key):
        return f'must mark all overloads with @overload: {key}'
