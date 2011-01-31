conf_py ='''\
# Configuration file for "%(title)s"
# Created by sffms-quickstart on %(now)s.
#
# -- Options for HTML output ---------------------------------------------------

# The remaining configuration values are either general Sphinx 
# settings, or settings for HTML and EPUB output. This configuration
# file is intentionally very minimal -- for basic HTML and EPUB output,
# you shouldn't have to change a thing. However, you can customize 
# this file much more heavily if need be. For more information, refer 
# to the Sphinx documentation at http://sphinx.pocoo.org/config.html.
#
# -- General configuration -----------------------------------------------------
#
extensions = ['sffms']
master_doc = '%(master_doc)s'
project = u'%(title)s'
copyright = u'%(copyright)s'
source_suffix = '.txt'

# -- Options for HTML output ---------------------------------------------------

html_theme = 'haiku'
html_title = u'%(title)s'
html_short_title = u'%(runningtitle)s'
html_static_path = ['_static']

# -- Options for EPUB output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'%(title)s'
epub_author = u'%(author)s'
epub_publisher = u'%(author)s'
epub_copyright = u'%(copyright)s'

'''