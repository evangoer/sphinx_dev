.. highlight:: console

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

01. Run :program:`sffms-quickstart` at the command line::

        $ sphinx-quickstart [<directory path>]

    If you provide an explicit directory path, :program:`sphinx-quickstart` 
    will generate the manuscript in that directory, creating the directory 
    if necessary. If you run :program:`sphinx-quickstart` with no arguments,
    it will prompt you for a directory path. If there is already a manuscript
    manuscript in the directory you provide, :program:`sphinx-quickstart` 
    prompts you for another path.
    
02. Answer :program:`sffms-quickstart`'s short list of questions. At a 
    minimum, you must indicate whether you are creating a short story or 
    novel and provide the author's name and a story title. It is a good idea 
    to provide an address, though this is not strictly required. 
    
    Once you finish answering the questions, :program:`sffms-quickstart` 
    generates a skeleton manuscript. If you exit the program prematurely
    by pressing :kbd:`CTRL-C`, no manuscript is generated.

03. Enter the manuscript directory. It contains these files:
    
    * :file:`Makefile` -- an infrastructure file that enables you to quickly
      and easily build your book. You should not need to edit this file.
      
    * :file:`conf.py` -- your manuscript's configuration file, which controls
      all sorts of aspects about how your book gets published. For more 
      information about these settings, refer to :ref:`configuration`. You 
      do not need to edit this file right away, but you will probably end 
      up modifying it in the future.

    * :file:`manuscript.txt` -- your manuscript's master file. If you are 
      writing a short story, this file should contain the entire contents
      of your story. If you are writing a novel, this file should contain
      a :rst:dir:`toctree` directive that points to individual chapter files.  
    
    * :file:`more_stuff.txt` (if you created a novel) -- an example 
      chapter file populated with random text.
    
    * :file:`new_chapter.txt` (if you created a novel) -- another example
      chapter file populated with random text.

04. At the command line, run::
    
        $ make sffmspdf
    
    This generates a number of files in the subdirectory :file:`_build/sffms`,
    including the file :file:`manuscript.pdf`. View this file.

Now you are ready to edit the master file and chapter files (if any) and 
run :program:`make sffmspdf` to view the effects of your changes. For more 
information about how to edit these files, refer to :ref:`markup`.