# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/utils.ipynb (unless otherwise specified).

__all__ = ['identity', 'simplify', 'listify', 'setify', 'tuplify', 'merge_tfms', 'compose', 'pipe', 'get_files',
           'function', 'T']

# Cell
from typing import Iterable, TypeVar, Generator
from plum import dispatch
from pathlib import Path
from functools import reduce

function = type(lambda: ())
T = TypeVar('T')

def identity(x: T) -> T:
    """Indentity function."""

    return x

def simplify(x):
    """Return an object of an iterable if it is lonely."""


    @dispatch
    def _simplify(x):
        if callable(x):
            try:
                return x()
            except TypeError:
                pass
        return x

    @dispatch
    def _simplify(i: Iterable): return next(i.__iter__()) if len(i) == 1 else i

    return _simplify(x)

def listify(x, *args):
    """Convert `x` to a `list`."""
    if args:
        x = (x,) + args

    if x is None:
        result = []
    elif isinstance(x, list): result = x
    elif isinstance(x, str) or hasattr(x, "__array__") or hasattr(x, "iloc"):
        result = [x]
    elif isinstance(x, (Iterable, Generator)):
        result = list(x)
    else:
        result = [x]

    return result


def setify(x, *args):
    """Convert `x` to a `set`."""

    return set(listify(x, *args))


def tuplify(x, *args):
    """Convert `x` to a `tuple`."""

    return tuple(listify(x, *args))


def merge_tfms(*tfms):
    """Merge two dictionnaries by stacking common key into list."""

    def _merge_tfms(tf1, tf2):
        return {
            k: simplify(listify(setify(listify(tf1.get(k)) + listify(tf2.get(k)))))
            for k in {**tf1, **tf2}
        }

    return reduce(_merge_tfms, tfms, dict())


def compose(*functions):
    """Compose an arbitrary number of functions."""

    def _compose(fn1, fn2):
        return lambda x: fn1(fn2(x))

    return reduce(_compose, functions, identity)


def pipe(*functions):
    """Pipe an arbitrary number of functions."""

    return compose(*functions[::-1])




def get_files(path, extensions=None, recurse=False, folders=None, followlinks=True):
    """Get all those file names."""
    path = Path(path)
    folders = listify(folders)
    extensions = setify(extensions)
    extensions = {e.lower() for e in extensions}

    def simple_getter(p, fs, extensions=None):
        p = Path(p)
        res = [
            p / f
            for f in fs
            if not f.startswith(".")
            and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)
        ]
        return res

    if recurse:
        result = []
        for i, (p, d, f) in enumerate(os.walk(path, followlinks=followlinks)):
            if len(folders) != 0 and i == 0:
                d[:] = [o for o in d if o in folders]
            else:
                d[:] = [o for o in d if not o.startswith(".")]
            if len(folders) != 0 and i == 0 and "." not in folders:
                continue
            result += simple_getter(p, f, extensions)
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        result = simple_getter(path, f, extensions)
    return list(map(str, result))
