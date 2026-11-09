"""Sphinx configuration for shifts-generator"""

from importlib.metadata import version as _version

project = "shifts-generator"
author = "Beatrice Saggiorato, Sara Beggiato"
release = _version("shifts-generator")

extensions = [
    "myst_parser",  # write pages in Markdown
    "sphinx.ext.autodoc",  # pull docstrings from the code
    "sphinx.ext.napoleon",  # understand Google-style docstrings
    "sphinx_autodoc_typehints",  # show type hints in the descriptions
    "sphinx.ext.intersphinx",  # link out to the Python and pandas docs
    "sphinx.ext.viewcode",  # optional "[source]" links
]

# automatic part: for now partially automatic (with automodule::, later it can be done with autosummary)
# list methods in specifi order: "bysource" - as they appear in the code, "groupwise" - by groupd (e.g. methods, properties),
# default is alphabetical
autodoc_member_order = "bysource"
# show classes of modules rather than modules alone
autodoc_default_options = {"members": True}

# doctrings convention
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# show a type for every parameter, even if not described in docstrings
always_document_param_types = True
# show default value in the parameter description (here with "comma" style)
typehints_defaults = "comma"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
}

# Make Markdown headings work as link targets (`[text](#heading)`).
# creates link targets for headings up to level 3
myst_heading_anchors = 3

html_theme = "furo"
html_title = "shifts-generator"

# Treat unresolved references as problems
nitpicky = True
nitpick_ignore_regex = [
    # ortools ships no intersphinx inventory, so its types can't be resolved.
    (r"py:class", r"ortools\..*"),
]
