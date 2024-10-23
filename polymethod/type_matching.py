#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict, UserDict, UserList, OrderedDict
from collections.abc import Iterable as IterableABC
from typing import Any, Dict, FrozenSet, List, Set, Tuple, Type, Union, Iterable, TypeVar
import inspect


def _type_hint_matches(obj, hint):
    if hint is inspect.Parameter.empty:
        # no type hint, we don't care
        return True
    try:
        if isinstance(hint, str):
            # type hint is a string, try to destringify it
            return isinstance(obj, destringify_annot(hint))
        if hint in [Any, object, ...]:
            # type hint says we don't care
            return True
        if hint is TypeVar:
            constraints = getattr(hint, '__constraints__', None)
            if constraints is None:
                return True
            return any(_type_hint_matches(obj, c) for c in constraints)
        return isinstance(obj, hint)
    except RuntimeError:
        return False
    except TypeError:
        origin = getattr(hint, '__origin__', None)
        if origin is None:
            return False
        if origin is Union:
            return any(_type_hint_matches(obj, arg) for arg in hint.__args__)
        try:
            if not isinstance(obj, origin):
                return False
            args = getattr(hint, '__args__', None)
            if args is None:
                return True
            if origin in [tuple, Tuple]:
                if not hasattr(obj, '__iter__'):
                    return False
                if any(arg is ... for arg in args):
                    return _type_hint_matches(obj[0], args[0])
                return len(args) == len(obj) and all(_type_hint_matches(o, a) for o, a in zip(obj, args))
            if origin in [dict, Dict, OrderedDict, defaultdict, UserDict]:
                if not isinstance(obj, dict):
                    return False
                return all(_type_hint_matches(k, args[0]) and _type_hint_matches(v, args[1]) for k, v in obj.items())
            if origin in [list, set, List, Set, FrozenSet, UserList, Iterable, IterableABC]:
                if isinstance(obj, str) or isinstance(obj, dict) or not hasattr(obj, '__iter__'):
                    return False
                return all(_type_hint_matches(o, args[0]) for o in obj)
            if origin in [type, Type]:
                return issubclass(obj, args[0])
            return True
        except TypeError:
            return False
        except RuntimeError:
            return False


def signature_matches(sig: inspect.Signature,
                      bound_args: inspect.BoundArguments):
    # doesn't handle type hints on *args or **kwargs
    for name, arg in bound_args.arguments.items():
        param = sig.parameters[name]
        hint = param.annotation
        if not _type_hint_matches(arg, hint):
            return False
    return True


def destringify_annot(annotation: str) -> Type:
    try:
        return eval(annotation)  # pylint: disable=eval-used
    except NameError as e:
        # cannot use annotation, try default
        raise RuntimeError("Cannot transform string annotation to type") from e
