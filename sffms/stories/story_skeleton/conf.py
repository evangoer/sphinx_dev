# To use this configuration file:
# 
# 1. Search and replace all instances of 'Your Name' 
# 2. Search and replace all instances of 'Your Title'
# 3. Go to the command line and run: 'sphinx-build -b sffms . _build'.
# 4. Change directory into '_build/sffms'. Run the command 'latex index.tex' -- twice.
# 5. Run the command 'pdflatex index.tex'.
# 
# You now have a PDF file in standard manuscript format. From here, you can:
# 
# * Modify the actual contents of 'index.txt'.
# * Play around with some of the other sffms options. Remember that some values
#   are commented out to show the default. Be sure to uncomment them first!
#
# This file also contains a set of minimal configuration options (general
# project info, HTML, and EPUB). Aside from replacing 'Your Name' and 
# 'Your Title', you do not need to change these settings for now. Later on,
# you can read up on those settings here: http://sphinx.pocoo.org/config.html

# -- General configuration -----------------------------------------------------

needs_sphinx = '1.0'
extensions = ['sffms']

exclude_patterns = ['_build']
templates_path = ['_templates']
master_doc = 'index'
source_suffix = '.txt'

project = u'Your Title'
copyright = u'2011, Your Name'
version = '1.0'
release = '1.0'

# -- Options for sffms output --------------------------------------------------

# REQUIRED. Sets the title.
sffms_title = 'Your Title'

# REQUIRED. Sets the author name.
sffms_author = 'Your Name'

# Provides a free-form multi-line address, telephone number, email address,
# or whatever contact info you wish to provide.
sffms_address = '''
123 Main Street
San Jose, CA 95128
(408) 555-1212
youremail@domain.com
'''

# If True, typesets this story as a novel. Top-level sections become chapters 
# instead of scenes, and each chapters starts a new page.
# sffms_novel = False 

# Tweaks the layout slightly according to a particular publisher's standards. Must 
# be set to one of: None, 'anon', 'baen', 'daw', or 'wotf'.
# sffms_submission_type = None     

# Changes the entire story to singlespaced, non-monospaced font.
# sffms_nonsubmission = False

# Removes the title page. Only works if sffms_nonsubmission = True.
# sffms_notitle = False

# Sets the title in running header. By default, sffms uses sffms_title. 
# Running headers often look nicer with a shorter version of your title.
# sffms_runningtitle = None

# Provides your real name for use with your mailing address, if that differs 
# from your nom de plume.
# sffms_authorname = None

# Sets your surname in the running header. By default, sffms uses sffms_author.
# Running headers often look nicer with your surname rather than your full name.
# sffms_surname = None 

# Overrides the entire running header with arbitrary LaTeX. Only use this option
# if you're really sure you know what you are doing.
# sffms_msheading = None

# Sets the paper size. Must be set to one of: None, 'a4paper', or 'letterpaper'. 
# If you are submitting to a U.S. publisher, leave this setting alone.
# sffms_papersize = None

# Changes the scene separator symbol from the default of "#".
# sffms_sceneseparator = None

# Changes the end-of-story symbol from the default of "# # # # #".
# sffms_thirty = None

# By default, sffms calculates a word count which is a "publisher's wordcount", 
# i.e. *not* the same as the word count you would get from Microsoft Office.
# If set to a number (sffms_wordcount = 12000), this overrides the calculated value.
# If set to None, this suppresses the word count entirely.
# sffms_wordcount = 'default'      

# If True, marks the document as disposable.
# sffms_disposable = False

# If True, inserts one space after sentences instead of two spaces.
# sffms_frenchspacing = False 

# If True, doublespaces blocks of verse & poetry. By default, verse is singlespaced.
# sffms_doublespace_verse = False

# Changes quote behavior. Must be one of: None, 'smart', 'dumb'. You should rarely change this.
# sffms_quote_type = None

# If True, overrides the default font and uses Courier instead. You should rarely change this.
# sffms_courier = False


# -- Options for HTML output ---------------------------------------------------

html_theme = 'haiku'
html_title = 'Your Title'
html_static_path = ['_static']
html_use_smartypants = True

# -- Options for Epub output ---------------------------------------------------

epub_title = u'sffms'
epub_author = u'Your Name'
epub_publisher = u'Your Name'
epub_copyright = u'2011, Your Name'

