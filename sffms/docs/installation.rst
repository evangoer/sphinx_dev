Installation and System Requirements
====================================

To set up your environment for sffms, you need working versions of:

* LaTeX
* The sffms LaTeX class
* Python 2.6 or 2.7
* Sphinx 1.0.5 or above

There are *many* ways to set up this environment. Following is a simple outline of 
what to do. 

 1. Install a `TeX distribution <http://www.tug.org/>`_ that includes LaTeX and 
    the `sffms LaTeX class <http://www.mcdemarco.net/sffms>`_. Popular TeX 
    distributions include:
        
    * Windows: `MiKTeX <http://www.miktex.org/>`_.
    * Most UNIX systems: `TeX Live <http://www.tug.org/texlive/>`_.
    * Mac OS X: `MacTeX <http://www.tug.org/mactex/>`_, which includes TeX Live.
    
    Once TeX is installed, you must make sure that the sffms LaTeX class is also 
    installed. DeMarco provides instructions under "Getting Started" in the 
    `user manual for the sffms LaTeX package <http://www.mcdemarco.net/sffms/class/sffms.pdf>`_.
    Your TeX distribution might already have sffms included and ready to go;
    check your documentation for more information.
    
 2. Verify that you can run :program:`latex` successfully on the source of one of 
    DeMarco's `example stories <http://mcdemarco.net/sffms/examples/>`_.
    
 3. Verify that you have Python 2.6 or Python 2.7 installed by typing 
    ``python --version`` at the command line. If necessary, you can 
    `download a suitable version <http://www.python.org/download/>`_ from
    python.org. As with TeX, there are many alternative ways to install Python.
    
    .. note:: The sffms Python package does not work with Python 3.

 4. Use :program:`easy_install` to install ``setuptools`` and ``pip``::
 
        $ sudo easy_install -U setuptools
        $ sudo easy_install -U pip

    Then use :program:`pip` to install the ``Sphinx`` and ``sffms`` Python packages::
 
        $ sudo pip install Sphinx
        $ sudo pip install sffms

Of course, if you are an advanced user, you can install these components any way
that seems sensible to you. For example, you might want to take advantage of your 
system's package management system to install TeX or Python, or use
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ to create an isolated 
Python environment.