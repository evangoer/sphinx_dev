Introduction
============

The `sffms Python package <http://pypi.python.org/pypi/sffms>`_ enables `sffms <http://www.mcdemarco.net/sffms/>`_ LaTeX output for `Sphinx <http://sphinx.pocoo.org/>`_. You can use this package to author short stories and novels in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ and publish the output through Sphinx.

Who is this package for?
------------------------

Let's suppose you're a really nerdy fiction writer. Nerdy enough to want to author in an open plain text format. Nerdy enough to want to check your files into a real version control system. Nerdy enough to run :program:`diff` and :program:`sed` and perform other text-munging feats of strength.

Sounds good in theory, but there's one major obstacle: `Standard Manuscript Format <http://www.sfwa.org/archive/writing/format_betancourt.htm>`_. Easy enough to produce with a word processor, but a huge pain if you prefer working with plain text. So what to do?

* Give up and use Word.
* Wait for the current generation of publishers and editors and all the people they have trained to die.
* Other.

This package is for the writers who choose "Other."

What are Sphinx and reStructuredText?
-------------------------------------

`reStructuredText <http://docutils.sourceforge.net/rst.html>`_ (aka reST) is a lightweight markup language developed by the Python community for technical documentation. `Sphinx <http://sphinx.pocoo.org/>`_ is a builder tool that transforms reST into different target output formats.

For the fiction writer, what Sphinx brings to the table is solid, easy to use HTML production. If you don't like the built-in HTML templates, it's straightforward to hack your own. Sphinx also produces EPUB out of the box, as should all writing tools worthy of your consideration.

Sphinx also produces LaTeX output. The problem with Sphinx's LaTeX output is that it's designed to typeset a nice looking technical manual, not a novel. Great for technical writers and software engineers, not so great for fiction writers. 

This is the problem that sffms solves.

What is sffms LaTeX?
--------------------

The `sffms <http://www.mcdemarco.net/sffms/>`_ LaTeX document class was developed by `M. C. DeMarco <http://www.mcdemarco.net/>`_ to typeset fiction manuscripts. It supports Standard Manuscript Format, including:

* a double-spaced manuscript in a 12-point monospaced font with one-inch margins 
* running headers of the form Author/TITLE/n, where n is the current page number
* a title page with the author's name and address in the upper left corner and a `publisher's word count <http://www.shunn.net/format/word_count/>`_ in the upper right
* correct typesetting for chapter and scene breaks
* conversion of italics, boldface, and small caps to appropriately underlined text
* many other niceties

All the ``sffms`` Python package does is glue Sphinx and sffms LaTeX together. When this extension is installed, Sphinx can convert your reStructuredText into LaTeX suitable for fiction instead of LaTeX suitable for technical documentation. 

Why not just write directly in LaTeX?
-------------------------------------

Maybe you should! Writing in LaTeX isn't actually that difficult, and DeMarco has `documented sffms <http://www.mcdemarco.net/sffms/class/sffms.pdf>`_ to the point where you can use sffms without actually knowing much about LaTeX itself. Even for non-experts, hand authoring a story in LaTeX is easier and cleaner than, say, hand authoring the same thing in HTML. It's all fairly civilized.

A minor point in reStructuredText's favor is that reST is a *little* easier to write in than LaTeX. reST's syntax is a little cleaner, and LaTeX has a number of reserved characters to watch out for. But if you're writing fiction, the mental overhead of working in either format is fairly close.

The bigger advantage of reStructuredText is that the LaTeX toolchain really only shines for print. TeX to HTML conversion tools are  uniformly kludgy and horrible, and they're particularly bad with sffms, which has some differences from a "normal" LaTeX manuscript that trip up most TeX to HTML converters.

So if all you care about is submitting manuscripts to publishers, you can just work in sffms LaTeX directly. But if you want anything even remotely reasonable to post to the web, you'll want to roll your own converter. Or read on.