Introduction
------------

This library is enables method overloading in Python
taking care of the method resolution without additional user required code
given sufficient typehints on the various functions.
It brings no additional requirements and can be easily integrated into existing
codebases.

License and Copyright Information
---------------------------------

This library is distributed under the MIT License, see ``LICENSE``.

Installation
------------

This project has no dependencies and can be installed with pip either locally

.. code-block:: bash

   git clone https://github.com/steinmig/polymethod.git
   pip install ./polymethod

or from PyPI

.. code-block:: bash

   pip install polymethod


Building documentation
----------------------

The dependencies for building the documentation can be installed with

.. code-block:: bash

   pip install -r docs/requirements.txt

The documentation can then be built and opened with

.. code-block:: bash

   sphinx-build docs/source docs/build
   firefox docs/build/index.html


Example Usage
-------------

This package allows you to overload functions, i.e. give multiple functions the same name,
but let them require different number and/or types of arguments.
This allows to provide simple APIs that can handle various inputs.
Currently, the overloading feature is limited to methods, i.e. functions of a class.
The overloaded methods can be regular methods, classmethods, or staticmethods.
An example class would be

.. code-block:: python

   from polymethod import overload, OverloadMeta, NoMatchingOverload
   from typing import Tuple

   class API(metaclass=OverloadMeta):

       @classmethod
       @overload
       def provide_id(cls, user_name: str) -> int:
           # some function body
           return 0

       @classmethod
       @overload
       def provide_id(cls, birthday: Tuple[int, int, int]) -> int:
           # another function body
           return 1

   assert API.provide_id("A user name") == 0
   assert API.provide_id((4, 7, 1776)) == 1
   try:
       API.provide_id(0)
   except NoMatchingOverload as e:
       print(str(e))

