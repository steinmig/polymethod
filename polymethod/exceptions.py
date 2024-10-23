#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class NoMatchingOverload(Exception):

    def __init__(self, *args, **kwargs) -> None:
        msg = "Could not determine a match for the given arguments:\n"
        if args:
            msg += ", ".join((repr(a) for a in args))
            msg += "\n"
        if kwargs:
            msg += ", ".join((f"{k}={v}" for k, v in kwargs.items()))
        super().__init__(msg)
