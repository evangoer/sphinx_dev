#!/usr/bin/env python

import sys, os, codecs

from sphinx.quickstart import do_prompt, boolean

conf_text ='''\
# This is a conf file. There are many 
# like it, but this one is mine.
'''

fields = {}

def main(argv):
    # write_conf_file()
    do_prompt(fields, 'hello', 'Say hello (y/N)', 'n', boolean)
    if fields['hello'] is True:
        print "Well HELLO!"
    else:
        print "Okay, fine then."
    
def write_conf_file():
    f = codecs.open('./conf.py', 'w', encoding='utf-8')
    f.write("HELLOSKI")
    f.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))