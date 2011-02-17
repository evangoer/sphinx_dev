Creating a New Manuscript
=========================

An sffms manuscript is actually a directory that contains a collection of files:

* a :file:`conf.py` file that provides metadata such as your name and address
* a master manuscript file that either contains your entire story, or contains references to separate chapter files
* one or more chapter files (if you are writing a multi-file story)
* a :file:`Makefile` that makes generating your story easier

Fortunately, you do not have to create these files by hand. The sffms package 
includes a program called :program:`sffms-quickstart` that prompts you with 
questions and then uses your answers to generate a skeleton manuscript for you.

To create a new manuscript:

1. Run :program:`sffms-quickstart` at the command line.

2. [TODO]