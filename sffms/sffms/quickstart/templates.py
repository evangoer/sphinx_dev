conf_py ='''\
# Configuration file for "%(title)s"
# Created by sffms-quickstart on %(now)s.
#
# -- Options for sffms output ---------------------------------------------------

# Sets the title. The title appears on the title page and in the 
# running header. This field is required.
sffms_title = u'%(title)s'

# Specifies whether to typeset this manuscript as a novel or as 
# a short story.
sffms_novel = %(novel)s

# Sets the author name. The author name appears on the title page  
# and in the running header. This field is required.
sffms_author = u'%(author)s'

# Provides a free-form multi-line address, which is typically a postal
# address, but could also include a phone number, email address, or any
# other contact info you wish to include. The address is displayed on the
# title page. This field is not required, but it is strongly recommended.
sffms_address = u\'\'\'%(address)s\'\'\'

# Provides your real name for use with your mailing address, if you are 
# using a pen name or are publishing under some variation of your name.
# sffms_authorname = None

# Changes the font to 12-point, 10-pitch Courier, as an alternative to 
# LaTeX’s default monospace font.
# sffms_courier = False

# Indicates whether the manuscript is disposable. When set to True, this
# field causes sffms to print “Disposable Copy” under the word count on 
# the title page.
# sffms_disposable = False

# Selects whether to doublespace lines of verse. When set to True, sffms 
# doublespaces lines of verse, just as it does ordinary paragraphs.
# sffms_doublespace_verse = False

# Indicates how to space between sentences. When set to True, sffms 
# inserts one space after sentences instead of two.
# sffms_frenchspacing = False

# Overrides the entire running header with arbitrary LaTeX. Only use 
# this option if you really know what you are doing. Don’t forget to 
# escape backslashes so that they will get passed to LaTeX correctly.
# sffms_msheading = None

# Changes the manuscript to be single spaced and use a non-monospaced 
# font, as with an ordinary LaTeX article or book.
# sffms_nonsubmission = False

# Removes the title page. This option only works if sffms_nonsubmission 
# is True.
# sffms_notitle = False

# Sets the paper size. Must be set to one of 'a4paper', 'letterpaper',
# or None (which is equivalent to 'letterpaper').
# sffms_papersize = None

# Controls how sffms handles "legacy" quotes, per the sffms LaTeX 
# documentation. Must be one of None, 'smart', or 'dumb'.
# sffms_quote_type = None

# Sets the title in the running header. Running headers usually look 
# nicer if you supply a shorter version of your title. 
sffms_runningtitle = u'%(runningtitle)s'

# Changes the scene separator string from "#" using plain text or 
# arbitrary LaTeX. 
# sffms_sceneseparator = None

# Adjusts the layout according to a particular publisher’s standards. 
# Must be set to one of: None, 'anon', 'baen', 'daw', 'wotf'.
# sffms_submission_type = None

# Sets your surname in the running header. Traditionally, running 
# headers use the author’s surname rather than their full name.
sffms_surname = u'%(surname)s'

# Controls the word count. When you you run latex on your manuscript, 
# this also generates an automatic word count. You can override this
# by setting sffms_wordcount to a number, or suppress the wordcount 
# entirely by setting this field to None.
# sffms_wordcount = 'default'

#
# The remaining configuration values are either general Sphinx 
# settings, or settings for HTML and EPUB output. These settings are
# intentionally very minimal -- for basic HTML and EPUB output,
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