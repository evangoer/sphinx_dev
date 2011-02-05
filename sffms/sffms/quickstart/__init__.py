import sys
import os
import time
import codecs

from sphinx.quickstart import do_prompt, boolean, is_path, ok, mkdir_p
from sphinx.util.console import bold

import templates

def main():
    fields = get_input()

    path = fields['path']
    if not os.path.isdir(path):
        mkdir_p(path)

    write_file(templates.conf_py % fields, path, 'conf.py')
    # TODO write makefile
    if fields['novel'] is True:
        write_file(templates.novel_ms % fields, path, fields['master_doc'] + '.txt')
        write_file(templates.novel_new_chapter, path, 'new_chapter.txt')
        write_file(templates.novel_more_stuff, path, 'more_stuff.txt')
    else:
        write_file(templates.story_ms % fields, path, fields['master_doc'] + '.txt')
        
    # TODO nicer interrupt behavior, like sphinx-quickstart

# TODO properly handle when optional fields are skipped/blank
def get_input():
    fields = {}

    print bold('Welcome to the sffms quickstart utility!')
    print '''
Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).'''
    
    print '''
Enter the directory in which to create your manuscript. The default
is this directory.'''
    prompt_path(fields)
    
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
    
    print '''
Your title appears in a running header at the top of the page.
If you have a long title, consider supplying a shorter version
for inclusion in the running header. For example, for the story
'The Adventures of Sherlock Holmes: A Scandal in Bohemia,' the
short version could be 'A Scandal in Bohemia.' '''
    do_prompt(fields, 'runningtitle', 'Enter your manuscript\'s short title (optional)', validator=optional)
    
    print ''
    do_prompt(fields, 'author', 'Enter your full name')
    
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
    do_prompt(fields, 'master_doc', 'Name of your master source file (without suffix)', 'manuscript')
    
    fields['now'] = time.asctime()
    fields['copyright'] = time.strftime('%Y') + ', ' + fields['author']
    return fields

def prompt_address(fields):
    """ Prompts for a multi-line address. If the user enters a blank line, we stop.
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
                fields['address'] = "'''" + fields['address'] + "'''"
            break
        else:
            if i > 1:
                fields['address'] += '\n'
            fields['address'] += fields[address_line].strip()
            i = i + 1
            
def prompt_path(fields):
    do_prompt(fields, 'path', 'Path to your manuscript', '.', is_path)
    while os.path.isfile(os.path.join(fields['path'], 'conf.py')):
        print bold('\nError: your path already has a conf.py.')
        print 'sffms-quickstart will not overwrite existing projects.\n'
        do_prompt(fields, 'path', 'Please enter a new path (or just Enter to exit)', '', is_path)
        if not fields['path']:
            sys.exit(1)

def optional(field):
    if field.strip() is '':
        return None
    else:
        return "'" + field + "'"

def generate_reST_title(title):
    bar = '#' * len(title)
    return bar + '\n' + title + '\n' + bar

def write_file(contents, path, filename):
    f = codecs.open(os.path.join(path, filename), 'w', encoding="utf-8")
    f.write(contents)
    f.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))