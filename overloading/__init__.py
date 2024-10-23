#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .api import overload, OverloadMeta
from .exceptions import NoMatchingOverload
from ._version import __version__  # noqa

_MISSING = object()

__all__ = ["overload", "OverloadMeta", "NoMatchingOverload"]
