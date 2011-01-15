import re
from addnodes import skip_me, pass_me, suppress_numbering
from docutils import nodes, writers
from sphinx.addnodes import start_of_file
from sphinx.util.compat import Directive

class SffmsWriter(writers.Writer):
    
    output = None  
    document = None

    def __init__(self, config):
        writers.Writer.__init__(self)
        self.config = config

    # at this point, the framework has set self.document by calling Writer.write()
    def translate(self):
        translator = SffmsTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()


class SffmsTranslator(nodes.NodeVisitor):
    
    body = []
    
    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config
        self.header = SffmsHeader(config)
        self.assign_node_handlers()

    def astext(self):
        return ''.join(self.body)
    
    def visit_Text(self, node):
        reserved_latex_chars = '[{}\\\^&\%\$#~_]'
        text = re.sub(reserved_latex_chars, self.escaped_chars, node.astext())
        self.body.append(text)
    
    def escaped_chars(self, match):
        if match.group(0) == '~':
            return '$\\sim$'
        elif match.group(0) == '\\':
            return '$\\backslash$'
        elif match.group(0) == '^':
            return '\\^{}'
        else:
            return '\\' + match.group(0)
    
    def depart_Text(self, node): pass
        
    def visit_paragraph(self, node):
        self.body.append('\n')
        
    def depart_paragraph(self, node):
        self.body.append('\n')
    
    def visit_section(self, node):
        '''
        Some funky logic to determine whether to emit a new chapter, a new scene, 
        or nothing. 
        
        This logic is even more confusing because even though we've inlined the 
        document, Sphinx does not adjust node.parent. This means whenever we refer to
        node.parent, we have to pretend that the doctree has not yet been inlined. 
                
        For now, this code makes no attempt to get the top-level section's title and
        use that as the document title. We're following the lead of all the default 
        Sphinx Builders and requiring the user to provide the document title as a 
        config value. That means duplication of information -- oh well. 
        '''
        
        # We do not actually want to emit a new scene or chapter for
        # the top-level section.
        if self.is_toplevel_section(node):
            pass
        elif self.is_new_chapter(node):
            self.body.append(self.new_chapter(node))
        else:
            self.body.append('\n\\newscene\n')
    
    def is_toplevel_section(self, node):
        ''' 
        If you are a section, and parent is a document with a 'docname' attribute, you are 
        the top-level section (unless the source markup is very malformed).
        '''
        if isinstance(node.parent, nodes.document) and 'docname' in node.parent:
            return True
        else:
            return False
        
    def is_new_chapter(self, node):
        '''
        Determines whether a section is a new chapter. Chapters are only relevant for novels. 
        The logic is slightly different depending on whether the novel is single-file or multi-file.
        '''
        if self.config.sffms_novel:
            # a multi-file novel with a toctree directive
            if isinstance(node.parent, nodes.document):
                return True
            # a single-file novel with chapters correctly nested under the top-level section
            elif isinstance(node.parent.parent, nodes.document) and 'docname' in node.parent.parent:
                return True
        else:
            return False

    def new_chapter(self, node):
        sn = node.next_node(condition=suppress_numbering)
        if isinstance(sn, suppress_numbering) and sn.parent is node:
            sn = '*'
        else:
            sn = ''
            
        title = node.next_node()
        if isinstance(title, nodes.title):
            return '\n\chapter' + sn + '{' + title.astext() + '}\n'
        else:
            raise SyntaxError("This chapter does not seem to have a title. That shouldn't be possible...")
    
    def depart_section(self, node): pass
    
    def visit_document(self, node):
        self.body.append(self.header.astext())
        self.body.append('\\begin{document}\n')
    
    def depart_document(self, node):
        self.body.append('\n\\end{document}\n')
    
    def visit_strong(self, node):
        self.body.append('\\textbf{')
    
    def depart_strong(self, node):
        self.body.append('}')
    
    def visit_emphasis(self, node):
        self.body.append('\emph{')
        
    def depart_emphasis(self, node):
        self.body.append('}')
    
    def visit_thought(self, node):
        self.body.append('\\thought{')
        
    def depart_thought(self, node):
        self.body.append('}')
    
    def visit_textsc(self, node):
        self.body.append('\\textsc{')

    def depart_textsc(self, node):
        self.body.append('}')
 
    def visit_line_block(self, node):
        if not self.config.sffms_doublespace_verse:
            self.body.append('\n\\begin{singlespace}')
        self.body.append('\n\\begin{verse}')
        
    def depart_line_block(self, node):
        self.body.append('\n\end{verse}\n')
        if not self.config.sffms_doublespace_verse:
            self.body.append('\\end{singlespace}\n')

    def visit_line(self, node):
        self.body.append('\n')
        
    def depart_line(self, node):
        '''
        Sffms requires us to insert two backslashes after each line of verse, *except*
        for blank lines and lines preceding blank lines.
        '''
        next_line = node.next_node(condition=nodes.line, siblings=1)
        if self.line_is_blank(node) and self.line_is_blank(next_line):
            self.body.append('\\\\')
    
    def line_is_blank(self, node):
        if not isinstance(node, nodes.line):
            return False
        else:
            return True if node.astext().strip() != '' else False
        
    def visit_block_quote(self, node):
        self.body.append('\n\\begin{quotation}')
        
    def depart_block_quote(self, node):
        self.body.append('\end{quotation}\n')
    
    def visit_synopsis(self, node):
        self.body.append('\n\\begin{synopsis}')
        
    def depart_synopsis(self, node):
        self.body.append('\\end{synopsis}\n')
        
    def assign_node_handlers(self):
        nodenames = [
            ('abbreviation', 'skip'),
            ('acks', 'skip'),
            ('admonition', 'skip'),
            ('attribution', 'skip'),
            ('bullet_list', 'skip'),
            ('caption', 'skip'),
            ('centered', 'skip'),
            ('citation', 'skip'),
            ('citation_reference', 'skip'),
            ('classifier', 'skip'),
            ('collected_footnote', 'skip'),
            ('colspec', 'skip'),
            ('comment', 'skip'),
            ('compact_paragraph', 'skip'),
            ('compound', 'pass'),
            ('container', 'skip'),
            ('decoration', 'skip'),
            ('definition', 'skip'),
            ('definition_list', 'skip'),
            ('definition_list_item', 'skip'),
            ('desc', 'skip'),
            ('desc_addname', 'skip'),
            ('desc_annotation', 'skip'),
            ('desc_content', 'skip'),
            ('desc_name', 'skip'),
            ('desc_optional', 'skip'),
            ('desc_parameter', 'skip'),
            ('desc_parameterlist', 'skip'),
            ('desc_returns', 'skip'),
            ('desc_signature', 'skip'),
            ('desc_type', 'skip'),
            ('description', 'skip'),
            ('docinfo', 'skip'),
            ('download_reference', 'skip'),
            ('entry', 'skip'),
            ('enumerated_list', 'skip'),
            ('field', 'skip'),
            ('field_list', 'skip'),
            ('figure', 'skip'),
            ('footer', 'skip'),
            ('footnote', 'skip'),
            ('footnote_reference', 'skip'),
            ('generated', 'skip'),
            ('glossary', 'skip'),
            ('header', 'skip'),
            ('highlightlang', 'skip'),
            ('hlist', 'skip'),
            ('hlistcol', 'skip'),
            ('image', 'skip'),
            ('index', 'skip'),
            ('inline', 'skip'),
            ('label', 'skip'),
            ('legend', 'skip'),
            ('list_item', 'skip'),
            ('literal', 'skip'),
            ('literal_block', 'skip'),
            ('literal_emphasis', 'skip'),
            ('meta', 'skip'),
            ('option', 'skip'),
            ('option_argument', 'skip'),
            ('option_group', 'skip'),
            ('option_list', 'skip'),
            ('option_list_item', 'skip'),
            ('option_string', 'skip'),
            ('pending_xref', 'skip'),
            ('problematic', 'skip'),
            ('production', 'skip'),
            ('productionlist', 'skip'),
            ('raw', 'skip'),
            ('refcount', 'skip'),
            ('reference', 'skip'),
            ('row', 'skip'),
            ('rubric', 'skip'),
            ('seealso', 'skip'),
            ('start_of_file', 'pass'),
            ('subscript', 'skip'),
            ('substitution_definition', 'skip'),
            ('substitution_reference', 'skip'),
            ('subtitle', 'skip'),
            ('superscript', 'skip'),
            ('suppress_numbering', 'pass'),
            ('system_message', 'skip'),
            ('table', 'skip'),
            ('tabular_col_spec', 'skip'),
            ('target', 'skip'),
            ('tbody', 'skip'),
            ('term', 'skip'),
            ('tgroup', 'skip'),
            ('thead', 'skip'),
            ('title', 'skip'),
            ('title_reference', 'skip'),
            ('topic', 'skip'),
            ('transition', 'skip'),
            ('versionmodified', 'skip')
        ]
        
        for name in nodenames:
            if name[1] == 'skip':
                setattr(self, 'visit_'+name[0], skip_me)
            elif name[1] == 'pass':
                setattr(self, 'visit_'+name[0], pass_me)
                setattr(self, 'depart_'+name[0], pass_me)
            else:
                raise ValueError("When assigning node handlers, you must set %s to either 'skip' or 'pass'." % name[0])
    
class SffmsHeader(object):
    """
    A helper class that uses sffms config values to generate the required LaTeX 
    documentclass and other LaTeX header commands. 
    """
    header = []
    
    def __init__(self, config):
        self.config = config
    
    def astext(self):
        """
        The command for generating the actual header text. Called in the translator
        during visit_document() (since after inlining the tree, there is only one document).
        """
        self.set_documentclass()
        self.set_command('title', self.config.sffms_title, required=True)
        self.set_command('runningtitle', self.config.sffms_runningtitle)
        self.set_command('author', self.config.sffms_author, required=True)
        self.set_command('authorname', self.config.sffms_authorname)
        self.set_command('surname', self.config.sffms_surname)
        self.set_address()
        self.set_wordcount()
        self.set_command('frenchspacing', self.config.sffms_frenchspacing, typ=bool)
        self.set_command('disposable', self.config.sffms_disposable, typ=bool)
        self.set_command('sceneseparator', self.config.sffms_sceneseparator)
        self.set_command('thirty', self.config.sffms_thirty)
        self.set_command('msheading', self.config.sffms_msheading)
        self.header.append('\n')
        return '\n'.join(self.header)

    def set_documentclass(self):
        r"""
        Handles all options [x,y,z] set for the document class. Output resembles::

          \documentclass[novel,baen]{sffms}
        
        This function enforces various restrictions on which options are allowed.
        """
        options = []

        if self.config.sffms_nonsubmission:
            options.append('nonsubmission')
            if self.config.sffms_notitle:
                options.append('notitle') 
        
        if self.config.sffms_novel:
            options.append('novel')

        sub_type = self.config.sffms_submission_type
        if sub_type: 
            if sub_type in ['anon', 'baen', 'daw', 'wotf']:
                options.append(sub_type)
            else:
                raise ValueError("If present, sffms_submission_type must be set to 'anon', 'baen', 'daw', or 'wotf'.")
                
        quote_type = self.config.sffms_quote_type
        if quote_type:
            if quote_type in ['smart', 'dumb']:
                options.append(quote_type)
            else:
                raise ValueError("If present, sffms_quote_type must be set to 'smart' or 'dumb'.")
        
        if self.config.sffms_courier:
            options.append('courier')
        
        # despite what the sffms LaTeX docs imply, I don't think sffms supports any other paper sizes.
        papersize = self.config.sffms_papersize
        if papersize == None:
            pass
        elif papersize in ['a4paper', 'letterpaper']:
            options.append('geometry')
            options.append(papersize)
        else:
            raise ValueError("If present, sffms_papersize must be set to 'a4paper' or 'letterpaper'.")
        
        options_str = ''
        if len(options) > 0:
            options_str = '[' + ','.join(options) + ']'
           
        self.header.append('\\documentclass' + options_str + '{sffms}')

    def set_command(self, name, value, typ=str, required=False):
        r"""
        Handles all simple header commands: string and boolean, required and optional.
        A string option resembles::
        
          \surname{Smith}
        
        A boolean option resembles::
        
          \frenchspacing
        """
        if value and isinstance(value, typ):
            if isinstance(value, str):
                self.header.append('\\' + name + '{' + value + '}')
            elif isinstance(value, bool):
                self.header.append('\\' + name)
        elif required:
            raise ValueError("You must provide a valid %s in your conf.py." % name)
    
    def set_address(self):
        """
        Sets the address properly. The address requires some funky logic where we need to
        add a LaTeX newline (two backslashes) after each line, *except* for the last line.
        """
        if not self.config.sffms_address:
            return

        address = self.config.sffms_address.splitlines()
        address_str = ''
        
        for i in range(0, len(address)):
            if (i < len(address) - 1): 
                address[i] += '\\\\\n'
            address_str += address[i]
            
        self.header.append('\\address{' + address_str + '}')

    def set_wordcount(self):
        """
        Sets the wordcount manually to a value (if set to a number) or turns off 
        the wordcount entirely (if set to None).
        """
        wc = self.config.sffms_wordcount
        if wc == None:
            self.header.append('\\wordcount{}')
        elif isinstance(wc, int):
            self.header.append('\\wordcount{%d}' % wc )
