# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = "apsimNGpy"
author = "richard magala"
copyright = "2025, richard magala"
release = "0.39.3.4"

# -- Path setup --------------------------------------------------------------
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]  # project root
sys.path.insert(0, str(ROOT))  # so autodoc can import your package

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    # "sphinx.ext.githubpages",  # only needed if not deploying via Actions
]

templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".apsimx",
    ".db",
]

# Autosummary/Autodoc
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "show-inheritance": True,
}
# Mock heavy/non-Linux deps so CI builds don’t choke
autodoc_mock_imports = ["pythonnet", "clr", "Models", "apsimNGpy.Models"]

# Autosectionlabel
autosectionlabel_prefix_document = True

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "rtd": ("https://docs.readthedocs.io/en/stable/", None),
}
intersphinx_disabled_domains = ["std"]

# Default role (so bare `name` links try smart resolution)
default_role = "any"

# Copybutton (strip prompts from copied code)
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True

# Optional: RST prolog (remove empty default-role directive)
rst_prolog = """
.. include:: <s5defs.txt>
"""

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- EPUB --------------------------------------------------------------------
epub_show_urls = "footnote"
