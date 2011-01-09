sffms LaTeX Extension for Sphinx
================================

Implements sffms-style LaTeX output for ReST + Sphinx, as specified by
http://www.mcdemarco.net/sffms/.

Sffms is a LaTeX document class for typesetting fiction manuscripts.
This is in contrast with the default Sphinx LaTeX Builder, which is 
designed for typesetting technical articles and manuals. The sffms 
Builder outputs "Standard Manuscript Format", 12-pt monospaced font 
with 1-inch margins and running headers. The package also exposes many 
configuration options for customizing your output.

You can use this package to author short stories and novels without 
having to write any raw LaTeX, while still taking advantage of Sphinx's 
flexible HTML and ePub capabilities.

.. note:: The sffms Builder only supports a small number of directives
          and roles that are appropriate for fiction writing, such as
          paragraphs, sections, and certain inline styles. The Builder
          ignores ReST elements that have no direct counterpart
          in the sffms specification.
