.. _configuration:

Configuration
=============

This section describes configuration values in ``conf.py``. At a minimum, you must specify:

* :ref:`master_doc`
* :ref:`sffms_author`
* :ref:`sffms_title`
* :ref:`sffms_address` (not strictly required, but strongly recommended)

You should also consider providing a surname and a running title:

* :ref:`sffms_surname`
* :ref:`sffms_runningtitle` (if your story title is long)

And if you are writing a novel as opposed to a short story, you must set :ref:`sffms_novel` to ``True``.

Beyond that, configuration values are up to you and your requirements.

.. _master_doc:

master_doc
----------

Example::

    master_doc = 'index.txt'

Specifies the name of your story's master document file. If you are writing
a single-file story, set this to be the file that contains your story.
If you are authoring a multi-file story, set this to be the file that contains 
the ``toctree`` directive.

.. note::

   The top-level section title in your master document file does not affect
   the title of your output PDF file -- this is set by :ref:`sffms_title`. 
   However, the top-level section title *does* appear if you build HTML or EPUB. 
   It is therefore good practice to make sure that the top-level section title 
   is the same as ``sffms_title``.

This field is **required**. 

.. _sffms_address:

sffms_address
-------------

Example:: 

    sffms_address = '''221b Baker Street
    London NW1
    United Kingdom
    arthur@conandoyle.com'''

Provides a free-form multi-line address, telephone number, email address,
or whatever contact info you wish to include. The address is displayed
on the title page.

You may provide explicit line breaks (``\n``) for each line, but it is 
better to just use a Python triple-quote (``'''``). The address is not 
required, but it is strongly recommended. 

By default, this field is ``None``, which prints no address at all.

.. _sffms_author:

sffms_author
------------

Example::

    sffms_author = 'Sir Arthur Conan Doyle'

Sets the author name. The author name appears on the title page and in 
the running header, although you can override this behavior with
:ref:`sffms_surname`, :ref:`sffms_authorname`, and 
:ref:`sffms_msheading`.

This field is **required**.

.. _sffms_authorname:

sffms_authorname
----------------

Example::

    sffms_authorname = 'Edward de Vere, 17th Earl of Oxford'

Provides your real name for use with your mailing address, if you are
using a pen name or are publishing under some variation of your name.
 
By default, this field is ``None``, which causes sffms to use 
:ref:`sffms_author` in the mailing address.


sffms_courier
-------------

Example::

    sffms_courier = True
    
Changes the font to 12-point, 10-pitch Courier. This might look better than 
LaTeX's default monospace font, depending on your local LaTeX setup. 
`DeMarco <http://mcdemarco.net>`_ recommends using this option if you want a 
fatter font than the default or if your PDF files are looking grainy. 

By default, this field is ``False``, which causes sffms to use the default 
LaTeX monospace font.


sffms_disposable
----------------

Example::

    sffms_disposable = True

Indicates whether the manuscript is disposable. When set to ``True``, 
this field causes sffms to print "Disposable Copy" under the word count
on the title page. This is useful if you are submitting a paper copy
of your manuscript and you want to let the publisher know explicitly that
you do not care if they mail the manuscript back to you.

By default, this field is ``False``. 


sffms_doublespace_verse
-----------------------

Example::

    sffms_doublespace_verse = True

Selects whether to doublespace lines of verse. When set to ``True``, 
sffms doublespaces lines of verse, just as it does ordinary paragraphs.

By default, this field is ``False``, which causes sffms to single-space
lines of verse.


.. _sffms_frenchspacing:

sffms_frenchspacing
-------------------

Indicates how to space between sentences. When set to ``True``, sffms
inserts one space after sentences instead of two. Whether to use one or 
two spaces is a matter of personal taste, although there are many 
extremely shouty people on the Internet who are willing to take time 
out of their busy day to convince you otherwise. 

By default, this field is ``False``, which causes sffms to use the
default LaTeX behavior of approximately two spaces between sentences. 


.. _sffms_msheading:

sffms_msheading
---------------

Example::

    sffms_msheading = '\\getsurname\\ /\\ \\getrunningtitle\\ /\\ \\pageofpages'
    
Overrides the entire running header with arbitrary LaTeX. Only use this option
if you really know what you are doing. Don't forget to escape backslashes so 
that they will get passed to LaTeX correctly.

To remove the running header entirely, set the heading to an empty string::

    sffms_msheading = ''

To have a running header that is just a page number::

    sffms_msheading = '\\thepage'
    
For page numbers of the form "Page 3 of 135"::

    sffms_msheading = '\\pageofpages'

To add more spacing between components::

    sffms_msheading = '\\getsurname\\ /\\ \\getrunningtitle\\ /\\ \\thepage'

By default, this field is ``None``. This is equivalent to setting ``sffms_msheading``
to:: 

    sffms_msheading = '\\getsurname/\\getrunningtitle/\\thepage'


.. _sffms_nonsubmission:

sffms_nonsubmission
-------------------

Example::

    sffms_nonsubmission = True

Changes the manuscript to be single spaced and use a non-monospaced 
font, as with an ordinary LaTeX article or book. sffms still generates
a title page, although you can suppress this with the :ref:`sffms_notitle`
option. 

By default, this field is ``False``, which generates the standard 
sffms-style double spacing and monospaced font. 


.. _sffms_notitle:

sffms_notitle
-------------

Example::

    sffms_notitle = False

Removes the title page. This option only works if :ref:`sffms_nonsubmission`
is ``True``. 

By default, this field is ``False``, which generates a title page.


.. _sffms_novel:

sffms_novel
-----------

Example:: 

    sffms_novel = True

Specifies whether to typeset this story as a novel or a short story. 
A short story begins on the title page, while a novel begins on a 
new page. In a novel, top-level sections become chapters instead of 
scenes, and each new chapter starts on a new page.

By default, this field is ``False``, which typesets your document as
a short story.


sffms_papersize
---------------

Example::

    sffms_papersize = 'a4paper'

Sets the paper size. If you are submitting to a U.S. publisher, you should 
probably ignore this setting. Must be set to one of:

    * ``None`` -- Equivalent to ``'letterpaper'``.
    * ``'a4paper'`` -- Sets the paper size to ISO 216 A4 (210 mm × 297 mm).
    * ``'letterpaper'`` -- Sets the paper size to ANSI A (8.5 in x 11 in).

By default, this field is ``None``.


sffms_quote_type
----------------

Example::

    sffms_quote_type = 'smart'

Controls how sffms handles "legacy" quotes. For more information, refer 
to the `sffms LaTeX documentation <http://www.mcdemarco.net/sffms/class/sffms.pdf>`_.
Must be one of:

  * ``None`` -- The default and recommended behavior.
  
  * ``'smart'`` -- Attempts to convert ordinary monospace-style ASCII quotation marks into LaTeX smart quotes.

  * ``'dumb'`` -- Attempts to convert LaTeX smart quotes into monospace-style ASCII quotation marks.

By default, this field is ``None``.


.. _sffms_runningtitle:

sffms_runningtitle
------------------

Example::

    sffms_runningtitle = 'A Scandal in Bohemia'

Sets the title in the running header. Running headers usually look nicer 
if you supply a shorter version of your title. For example, rather than 
'The Adventures of Sherlock Holmes: A Scandal in Bohemia', you can set 
the running title to simply be 'A Scandal in Bohemia'. 
See also :ref:`sffms_authorname`.

By default, this field is ``None``, which causes sffms to use 
:ref:`sffms_title` in the running title. 


sffms_sceneseparator
--------------------

Example::

    sffms_sceneseparator = '$\\star\\star\\star\\star\\star$'

Changes the scene separator string from '#', using plain text or even
arbitrary LaTeX. The example above would change the scene separator 
to five star characters. Don't forget to escape backslashes so that 
they will get passed to LaTeX correctly.

By default, this field is ``None``, which causes sffms to use 
the default scene separator of a centered hash mark. 


sffms_submission_type
---------------------

Example::

    sffms_submission_type = 'daw'

Adjusts the layout according to a particular publisher's standards. 
Must be set to one of: 

  * ``None`` -- Uses the default layout. This is the correct option
    for most manuscripts.
  
  * ``'anon'`` -- Removes all information about the author, to comply
    with certain contests and venues that require anonymous submissions.

  * ``'baen'`` -- Increases margins from 1" to 1 1/2". Refer to the
    `Baen submission guidelines <http://www.baen.com/FAQS.htm>`_.
  
    .. note:: Baen submission guidelines currently require electronic
              submissions in RTF, not PDF.

  * ``'daw'`` -- Typesets the address and wordcount on the right-hand
    side of the first page rather than splitting it across the page. Refer to the
    `Daw submission guidelines <http://us.penguingroup.com/static/html/daw/submissions.html>`_.

  * ``'wotf'`` -- Uses a full cover page for short stories, omits the
    author's surname from the running header, uses the story's full title 
    in the running header, and begins page numbering with the first story
    page. Refer to the 
    `Writers of the Future submission guidelines <http://wof.webstudioswest.com/contest-rules>`_

By default, this field is ``None``, which uses the default layout.


.. _sffms_surname:

sffms_surname
-------------

Example::

    sffms_surname = "Doyle" 

Sets your surname in the running header. Traditionally, running headers
use the author's surname rather than their full name. 

By default, this field is ``None``, which causes sffms to use 
:ref:`sffms_author` in the running title.


sffms_thirty
------------

Example::

    sffms_thirty = 'The End'

Changes the end-of-story symbol from the default of '# # # # #', 
using plain text or even arbitrary LaTeX. Don't forget to escape 
backslashes so that they will get passed to LaTeX correctly.

By default, this field is ``None``, which causes sffms to use 
the default scene separator of a centered hash mark.


.. _sffms_title:

sffms_title
-----------

Example::

    sffms_title = 'The Adventures of Sherlock Holmes: A Scandal in Bohemia'

Sets the title. The title appears in the title page and the running header, 
although you can override this behavior with :ref:`sffms_runningtitle`. 

This field is **required**.


sffms_wordcount
---------------

Example::

    sffms_wordcount = 12000

Controls the word count. When you you run **latex** on your 
manuscript, this also generates an automatic word count. Note that this 
is a `publisher's word count <http://www.shunn.net/format/word_count/>`_, 
which is *not* the same thing as the word count generated by Microsoft 
Word and similar tools. 

.. note:: To get a sensible automatic word count, the first time you
          run your manuscript through **latex**, you must run **latex** 
          twice.

The author of the sffms LaTeX class derived her word count formula
from the contents of one of her own stories, as described in the 
`sffms LaTeX documentation <http://www.mcdemarco.net/sffms/class/sffms.pdf>`_.
The results are reasonable, but you can always use ``sffms_wordcount`` to 
set the word count to a particular number based on your own calculations. 
Alternatively, you can suppress the wordcount by setting this field to ``None``.

By default, this field is set to the string 'default', which uses
the automatic word count formula. 