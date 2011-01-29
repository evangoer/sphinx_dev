#!/usr/bin/env python

import sys, os, codecs

conf_text ='''\
# This is a conf file. There are many 
# like it, but this one is mine.
'''

def main(argv):
    write_conf_file()
    
def write_conf_file():
    f = codecs.open('./conf.py', 'w', encoding='utf-8')
    f.write("HELLOSKI")
    f.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))