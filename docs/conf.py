import sphinx_rtd_theme
import os, sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

sys.path.insert(0, os.path.abspath('../src'))

project = 'Tihi'
copyright = '2024, Kyunghoon Han'
author = 'Kyunghoon Han'
release = '0.0.4'
version = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
]

templates_path = ['_templates']
exclude_patterns = []

source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = []
html_favicon = "../src/tihi/icons/64.png"
htmlhelp_basename = '{}doc'.format(project)