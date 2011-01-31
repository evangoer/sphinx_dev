import sys
import os
import time
import codecs

from sphinx.quickstart import do_prompt, boolean, is_path, ok
from sphinx.util.console import bold

import templates


def main():
    fields = get_input()
    print templates.conf_text % fields
    # write_conf_file()
    # TODO nicer interrupt behavior, like sphinx-quickstart


def get_input():
    fields = {}

    print bold('Welcome to the sffms quickstart utility')
    print '''
Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).'''
    
    print '''
Enter the directory in which to create your manuscript.'''
    do_prompt(fields, 'path', 'Path to your manuscript', '.', is_path)
    
    print '''
You can use this script to set up a novel or a short story.
For novels, sffms-quickstart creates a master story file and 
three chapter files, while for short stories, sffms-quickstart 
generates a single master story file. Short stories are also 
typeset a little differently from novels.'''
    do_prompt(fields, 'novel', 'Are you creating a novel? (y/N)', 'n', boolean)

    print ''
    do_prompt(fields, 'title', 'Enter your manuscript\'s title')
    
    print '''
Your title appears in a running header at the top of the page.
If you have a long title, consider supplying a shorter version
for inclusion in the running header. For example, for 
'The Adventures of Sherlock Holmes: A Scandal in Bohemia,' 
the short version could be 'A Scandal in Bohemia.' '''
    do_prompt(fields, 'runningtitle', 'Optionally enter your manuscript\'s short title', validator=ok)
    
    print ''
    do_prompt(fields, 'author', 'Enter your name')
    
    print '''
Your full name (or surname, if specified) appears in the 
running header. Consider supplying your surname here.'''
    do_prompt(fields, 'surname', 'Optionally enter your surname', validator=ok)
    
    # what is your address? (some kind of loop)

    print '''
Your story source is contained in a master file. This file
either contains the entire story, or a table of contents
that points to separate chapter files.'''
    do_prompt(fields, 'master_doc', 'Name of your master source file (without suffix)', 'manuscript')
    
    fields['now'] = time.asctime()
    fields['copyright'] = time.strftime('%Y') + ', ' + fields['author']
    return fields

def write_conf_file():
    f = codecs.open('./conf.py', 'w', encoding='utf-8')
    f.write("HELLOSKI")
    f.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))