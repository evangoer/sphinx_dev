import re
from docutils import nodes, writers
from docutils.io import StringOutput
from sphinx.addnodes import start_of_file
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees

def setup(app):
    
    # If true, opens up the 'notitle' option.
    app.add_config_value('sffms_nonsubmission', False, '')
    
    # If true, opens up the possibility of having a synopsis.
    app.add_config_value('sffms_novel', False, '')
    
    # Should be one of: anon, baen, daw, wotf
    app.add_config_value('sffms_submission_type', None, '')

    # Should be one of: smart, dumb, None. 
    app.add_config_value('sffms_quote_type', None, '')

    # Removes the title page. Only usable when submission type is 'nonsubmission'.
    app.add_config_value('sffms_notitle', False, '')
    
    # Overrides the default monospace font.
    app.add_config_value('sffms_courier', False, '')

    # Advanced option, not yet implemented (see papersize below)
    app.add_config_value('sffms_geometry', False, '')
    
    # 'If you use geometry with the intent of fixing your paper size, you should declare the paper size explicitly.'
    # Figure out what DeMarco is saying here. Can I declare this if geometry = False? Is it required if geometry = True? 
    # Possible values are 'a4paper', 'letterpaper', and others as defined in the geometry package.
    app.add_config_value('sffms_papersize', None, '')

    # Required.
    app.add_config_value('sffms_title', None, '')
    
    # Optional. sffms uses the title in place of the running title if it is absent.
    app.add_config_value('sffms_runningtitle', None, '')
    
    # Required.
    app.add_config_value('sffms_author', None, '')
    
    app.add_config_value('sffms_authorname', None, '')
    app.add_config_value('sffms_surname', None, '')
    
    # In sffms, this is a free-form multi-line piece of text. Need to think how to specify it. Triple quotes?
    app.add_config_value('sffms_address', None, '')
    
    # Set the wordcount manually to some numeric value. Can also set to be None, to suppress completely.
    app.add_config_value('sffms_wordcount', 'default', '')

    app.add_config_value('sffms_disposable', False, '')
    app.add_config_value('sffms_frenchspacing', False, '')

    # New config values not directly in sffms
    app.add_config_value('sffms_doublespace_verse', False, '')
    
    app.add_builder(SffmsBuilder)

class SffmsBuilder(Builder):
    """
    Builder for sffms-style LaTeX. Totally different output
    from the default Sphinx LaTeX builder.
    """
    
    name = "sffms"
    format = "latex"
    out_suffix = ".tex"
    writer = None
    
    # Could copy image list from LaTeXBuilder. But for now, images aren't supported.
    supported_image_types = []  
    
    # TODO grab initial sffms configuration
    def init(self):
        pass
    
    def get_outdated_docs(self):
        return 'all documents'
    
    def prepare_writing(self, docnames):
        self.writer = SffmsWriter(self.config)
    
    def get_relative_uri(self, from_, to, typ=None):
        return self.get_target_uri(to, typ)
    
    # LaTeXBuilder has slightly more complicated behavior here, might need to copy wholesale    
    def get_target_uri(self, docname, typ):
        return '%' + docname

    # Overriding the default write() implementation because we must write to
    # a single file in TOC order. So rather than getting write_doc() called for us
    # multiple times, we assemble one big inline doctree and call write_doc() once.
    # 
    # Code adapted from SinglePageHTML, since that seems to be the simplest implementation.
    def write(self, *ignored):
        docnames = self.env.all_docs

        self.info(bold('preparing documents...'), nonl=True)
        self.prepare_writing(docnames)
        self.info('done')

        self.info(bold('assembling single document... '), nonl=True)
        doctree = self.assemble_doctree()
        self.info()
        self.info(bold('writing... '), nonl=True)
        self.write_doc(self.config.master_doc, doctree)
        self.info('done')
        
    def assemble_doctree(self):
        master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set() , master, tree, darkgreen)
        tree['docname'] = master
        print tree.pformat()
        
        # skip code that checks references, etc.
        return tree
    
    def write_doc(self, docname, doctree):
        # print doctree.pformat()
        destination = StringOutput(encoding='utf-8')
        output = self.writer.write(doctree, destination)
        print output
    

class SffmsWriter(writers.Writer):
    
    # a writer has a self.output = None, which is then set by calling translate()
    output = None
    
    # a writer has a self.document = None, which is then set by calling write()
    document = None

    def __init__(self, config):
        writers.Writer.__init__(self)
        self.config = config

    # at this point, self.document has been set by write()
    def translate(self):
        translator = SffmsTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()


class SffmsTranslator(nodes.NodeVisitor):
    
    body = []    
    reserved_latex_chars = '[{}\\\^&\%\$#]'
    
    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config
        self.header = SffmsHeader(config)
        self.assign_node_handlers()

    def astext(self):
        return ''.join(self.body)
    
    def visit_Text(self, node):
        text = re.sub(self.reserved_latex_chars, self.escaped_chars, node.astext())
        self.body.append(text)
    
    def escaped_chars(self, match):
        return '\\' + match.group(0)
    
    def depart_Text(self, node): pass
        
    def visit_paragraph(self, node):
        self.body.append('\n')
        
    def depart_paragraph(self, node):
        self.body.append('\n')
    
    # Here is where we need to figure out \newscene, \chapter, and titles.
    # Answer is different depending on whether we are a novel or a short story,
    # and what our parent is.
    #
    # If our parent is a document: 
    # - if we are a novel, start a new chapter
    # - if we are a short story, start a new scene
    # If our parent is a document and is the master_doc: 
    # - child paras below me are a synopsis?
    #   - no, probably too much magic there. Declare a synopsis explicitly with a custom directive.
    # - in any case, don't emit a new chapter or new scene?
    #   - no, leave this alone. Need to support the single-file use case
    # - Might want to grab thestory title from this section, though
    #   - user probably would be surprised to have the title ignored
    #   - probably want: take the title from the text itself
    #   - fall back to conf.py
    #   - if title specified nowhere, throw an error
    # 
    # Otherwise:
    # - start a new scene
    #
    # We have to require a title at the top of each page for compatibility with
    # the HTML builder. You can't just bang out some text without having a title
    # for each file. You'll still get some output if you do this, but the behavior
    # is undefined.
    # 
    # How does that affect short story authoring?
    # Note: it is perfectly okay to have a single 'index.txt' file that includes 
    # no files and has no toctree!
    #
    # TODO decide what the behavior is and untangle this silly nesting
    def visit_section(self, node):
        # if isinstance(node.parent, nodes.document):
        #    pass
        if isinstance(node.parent, nodes.document):
            if 'docname' in node.parent:  # we are in the master_doc
                pass
            else:                         # we are just in a document 
                if self.config.sffms_novel:
                    self.new_chapter(node)
                else:
                    self.body.append('\n\\newscene\n')
        else:
            self.body.append('\n\\newscene\n')

    def new_chapter(self, node):
        title = node.next_node()
        if isinstance(title, nodes.title):
            self.body.append('\n\chapter{' + title.astext() + '}\n')
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

    def visit_literal(self, node):
        if 'kbd' in node['classes']:
            self.body.append('\\textsc{')
        else:
            self.body.append('\\thought{')
            
    def depart_literal(self, node):
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
                setattr(self, 'visit_'+name[0], self.default_skip_handler)
            elif name[1] == 'pass':
                setattr(self, 'visit_'+name[0], self.default_pass_handler)
                setattr(self, 'depart_'+name[0], self.default_pass_handler)
            else:
                raise ValueError("When assigning node handlers, you must set %s to either 'skip' or 'pass'." % name[0])

    def default_pass_handler(self, node): pass

    def default_skip_handler(self, node): raise nodes.SkipNode
    
class SffmsHeader(object):
    '''
    A helper class that uses sffms config values to generate the required LaTeX 
    documentclass and other header commands. 
    '''
    
    header = []
    
    def __init__(self, config):
        self.config = config
    
    def astext(self):
        '''
        The command for generating the actual header text. In our case, we call
        this method in the translator, during visit_document() (since after inlining
        the tree, there is only one document).
        '''
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
        self.header.append('\n')
        return '\n'.join(self.header)

    def set_documentclass(self):
        '''
        Handles all options [x,y,z] set for the document class. Output resembles::

          \documentclass[novel,baen]{sffms}
        
        This function enforces various restrictions on which options are allowed.
        '''
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
        
        options_str = ''
        if len(options) > 0:
            options_str = '[' + ','.join(options) + ']'
           
        self.header.append('\\documentclass' + options_str + '{sffms}')

    def set_command(self, name, value, typ=str, required=False):
        '''
        Handles all simple header commands: string and boolean, required and optional.
        A string option resembles::
        
          \\surname{'Smith'}
        
        A boolean option resembles::
        
          \\frenchspacing
        '''
        if value and isinstance(value, typ):
            if isinstance(value, str):
                self.header.append('\\' + name + '{' + value + '}')
            elif isinstance(value, bool):
                self.header.append('\\' + name)
        elif required:
            raise ValueError("You must provide a valid %s." % name)
    
    def set_address(self):
        '''
        Sets the address properly. The address requires some funky logic where we need to
        add a LaTeX newline (two backslashes) after each line, *except* for the last line.
        '''
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
        '''
        Sets the wordcount manually to a value (if set to a number) or turns off 
        the wordcount entirely (if set to None).
        '''
        wc = self.config.sffms_wordcount
        if wc == None:
            self.header.append('\\wordcount{}')
        elif isinstance(wc, int):
            self.header.append('\\wordcount{%d}' % wc )

