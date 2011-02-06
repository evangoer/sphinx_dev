import sys
import os
import time
import codecs

from sphinx.quickstart import do_prompt, boolean, is_path, ok, mkdir_p
from sphinx.util.console import bold

import sffms.quickstart.templates

def main():
    if len(sys.argv) > 2:
        print 'Usage: sffms-quickstart [manuscript_directory]'
        sys.exit(1)
    try:
        sys.exit(inner_main(argv=sys.argv))
    except (KeyboardInterrupt, EOFError):
        print
        print '[Interrupted.]'
        sys.exit(1)

def inner_main(argv):
    fields = {}
    
    get_input(fields, argv)
    make_path(fields['path'])
    
    write_file(templates.conf_py % fields, fields['path'], 'conf.py')
    write_file(templates.makefile, fields['path'], 'Makefile')
    write_skeleton_files(fields)
    
    print_success(fields)
    return 0

def get_input(fields, argv):
    print bold('Welcome to the sffms quickstart utility!')
    print '''
Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).'''
    
    fields['path'] = get_path_from_cmdline(argv)
    if fields['path'] is None:
        print '''
Enter the directory in which to create your manuscript. The default
is this directory.'''
        do_prompt(fields, 'path', 'Path to your manuscript', '.', is_path)
    get_clear_path(fields)
        
    print '''
You can use this script to set up a novel or a short story.
For novels, sffms-quickstart creates a master story file and 
three chapter files, while for short stories, sffms-quickstart 
generates a single master story file. Short stories are also 
typeset a little differently from novels.'''
    do_prompt(fields, 'novel', 'Are you creating a novel? (y/N)', 'n', boolean)

    print ''
    do_prompt(fields, 'title', 'Enter your manuscript\'s title')
    fields['reST_title'] = generate_reST_title(fields['title'])
    # We sanitize the title after creating the 'reST_title' because we 
    # don't actually want to escape those characters in reST -- just in Python.
    fields['title'] = py_sanitize(fields['title'])
    
    print '''
Your title appears in a running header at the top of the page.
If you have a long title, consider supplying a shorter version
for inclusion in the running header. For example, for the story
'The Adventures of Sherlock Holmes: A Scandal in Bohemia,' the
short version could be 'A Scandal in Bohemia.' '''
    do_prompt(fields, 'runningtitle', 'Enter your manuscript\'s short title (optional)', validator=optional)
    
    print ''
    do_prompt(fields, 'author', 'Enter your full name', validator=py_sanitize)
    
    print '''
Your full name (or surname, if specified) appears in the 
running header. Consider supplying your surname here.'''
    do_prompt(fields, 'surname', 'Enter your surname (optional)', validator=optional)
    
    print '''
You may enter a free-form multi-line address, including a postal 
address, telephone number, email address, or whatever contact info 
you wish to include. The address is displayed on the title page. 
When you are done entering the address, enter an empty (blank) line.'''
    prompt_address(fields)

    print '''
Your story source is contained in a master file. This file
either contains the entire story, or a table of contents
that points to separate chapter files.'''
    do_prompt(fields, 'master_doc', 'Name of your master source file (without suffix)', 'manuscript', validator=py_sanitize)
            
    fields['now'] = time.asctime()
    fields['copyright'] = time.strftime('%Y') + ', ' + fields['author']
    
def py_sanitize(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")

def get_path_from_cmdline(argv):
    if len(argv) == 2 and is_path(argv[1]):
        return argv[1]
    else:
        return None

def get_clear_path(fields):
    while os.path.isfile(os.path.join(fields['path'], 'conf.py')):
        print bold('\nError: your path already has a conf.py.')
        print 'sffms-quickstart will not overwrite existing projects.\n'
        do_prompt(fields, 'path', 'Please enter a new path (or just Enter to exit)', '', is_path)
        if not fields['path']:
            sys.exit(1)

def prompt_address(fields):
    """ 
    Prompts for a multi-line address. If the user enters a blank line, we stop.
    If the user enters a blank line on the first entry, we set the address to None.
    Otherwise, we build the address up up line by line.
    """
    i = 1
    fields['address'] = ''
    while True:
        address_line = 'address{0}'.format(i)
        do_prompt(fields, address_line, 'Enter address line {0}'.format(i), validator=ok)
        if fields[address_line].strip() is '':
            if i == 1:
                fields['address'] = None
            else:
                fields['address'] = "'''" + py_sanitize(fields['address']) + "'''"
            break
        else:
            if i > 1:
                fields['address'] += '\n'
            fields['address'] += fields[address_line].strip()
            i = i + 1
            
def optional(field):
    if field.strip() is '':
        return None
    else:
        return "'" + py_sanitize(field) + "'"

def generate_reST_title(title):
    bar = '#' * len(title)
    return bar + '\n' + title + '\n' + bar

def make_path(path):
    if not os.path.isdir(path):
        mkdir_p(path)

def write_file(contents, path, filename):
    f = codecs.open(os.path.join(path, filename), 'w', encoding="utf-8")
    f.write(contents)
    f.close()

def write_skeleton_files(fields):
    path = fields['path']
    if fields['novel'] is True:
        write_file(templates.novel_ms % fields, path, fields['master_doc'] + '.txt')
        write_file(templates.novel_new_chapter, path, 'new_chapter.txt')
        write_file(templates.novel_more_stuff, path, 'more_stuff.txt')
    else:
        write_file(templates.story_ms % fields, path, fields['master_doc'] + '.txt')

def print_success(fields):
    print 
    print bold('Finished: Initial manuscript files created in directory \n%s.' % os.path.abspath(fields['path']))
    print
    if fields['novel'] is True:
        print 'You should now begin adding material to your chapter .txt files.'
        print 'To add new chapters or change their filenames, edit %s.txt.' % fields['master_doc']
    else:
        print 'You should now begin adding material to %s.txt.' % fields['master_doc']
    print 'To generate PDF, run the command ' + bold('make sffmspdf') + ' in the directory.'
    print 'Happy writing!'
    
    