#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sphinx_rtd_theme
import overloading
import recommonmark
import sys
import pathlib
from recommonmark.transform import AutoStructify

project = "overloading"
copyright = "James Murphy (MCODING LLC)"
author = "Miguel Steiner"

version = overloading.__version__
release = overloading.__version__

source_suffix = ['.rst']
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'numpydoc',
    'sphinx_copybutton',
]
plot_html_show_source_link = False
plot_html_show_formats = False
autosummary_generate = True
numpydoc_show_class_members = False
master_doc = 'index'
language = "en"
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
    ]
}
htmlhelp_basename = 'overloading'

latex_documents = [
    (master_doc, 'overloading.tex', 'overloading Documentation',
     'Contributors', 'manual'),
]

man_pages = [
    (master_doc, 'overloading', 'overloading Documentation',
     [author], 1)
]


texinfo_documents = [
    (master_doc, 'overloading', 'overloading Documentation',
     author, 'overloading', 'Python package for overloading methods of the same name.',
     'Miscellaneous'),
]

autodoc_default_options = {
    "autosummary": True,
    "members": True,
    "undoc-members": True,
    "inherited-members": True,
    "class-doc-from": "both",
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
}
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())
