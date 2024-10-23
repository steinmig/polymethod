from os import path
from setuptools import setup, find_packages
import sys


min_version = (3, 6)
if sys.version_info < min_version:
    error = """
Polymethod does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(
        *(sys.version_info[:2] + min_version)
    )
    sys.exit(error)

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'polymethod', '_version.py')) as f:
    exec(f.read())


setup(
    name="polymethod",
    version=__version__,
    description="Library to enable function polymethod in Python",
    long_description=readme,
    author="Miguel Steiner",
    author_email="steiner.mig@gmail.com",
    python_requires=">={}".format(".".join(str(n) for n in min_version)),
    packages=find_packages(include=["polymethod", "polymethod.*"],
                           exclude=["polymethod.tests*"]),
    install_requires=[],
    license="MIT",
    license_files = ('LICENSE',),
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    zip_safe=True,
    test_suite="pytest",
    tests_require=["pytest"],
)
