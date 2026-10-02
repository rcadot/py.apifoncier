"""Configuration Sphinx de la documentation ``apifoncier``.

Référence : https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import apifoncier

# -- Informations sur le projet ----------------------------------------------

project = "apifoncier"
copyright = "2023-2026, Romain Cadot"
author = "Romain Cadot"
release = apifoncier.__version__
version = release

# -- Configuration générale ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "nbsphinx",
]

# Libellés automatiques limités aux titres de page : les titres de section
# (« Présentation », « Import »...) se répètent d'une page à l'autre.
autosectionlabel_maxdepth = 1
autodoc_typehints = "description"
autodoc_member_order = "bysource"
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Les notebooks d'exemple ne sont pas ré-exécutés lors de la construction.
nbsphinx_execute = "never"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "fr"

# -- Sortie HTML ---------------------------------------------------------------

html_theme = "piccolo_theme"
html_static_path: list = []
html_theme_options = {
    "source_url": "https://github.com/rcadot/py.apifoncier",
    "source_icon": "github",
}
