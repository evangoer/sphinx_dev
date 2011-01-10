import re, codecs
from os import path
from docutils import nodes, writers
from docutils.io import StringOutput
from sphinx.addnodes import start_of_file
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

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

    # Possible values are 'a4paper' and 'letterpaper'.
    app.add_config_value('sffms_papersize', None, '')
    
    # Changes the scene separator from "#" to something else.
    app.add_config_value('sffms_sceneseparator', None, '')

    # Changes the end-of-story symbol from "# # # # #" to something else. 
    app.add_config_value('sffms_thirty', None, '')
    
    # Overrides the default manuscript heading with different LaTeX content. 
    app.add_config_value('sffms_msheading', None, '')

    # Required.
    app.add_config_value('sffms_title', 'How I Forgot To Set My sffms_title In My conf.py: A Memoir', '')
    
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
    
    # Suppress specific chapter numbering for specific chapters. Make sure that we don't make 
    # the default Sphinx builders fall over when they encounter an unknown node.
    app.add_node(suppress_numbering, html=(skip_me, None), latex=(skip_me, None),
        text=(skip_me, None), man=(skip_me, None))
    app.add_directive('suppress_numbering', SffmsSuppressNumberingDirective)
    
    # Allow the user to add a synopsis section anywhere in the document. Pass it through to
    # the default Sphinx builders and hope it looks okay.
    app.add_node(synopsis, html=(pass_me, pass_me), latex=(pass_me, pass_me),
        text=(pass_me, pass_me), man=(pass_me, pass_me))
    app.add_directive('synopsis', SffmsSynopsisDirective)
    
    # Add two inline styles defined by sffms (thought and textsc)
    app.add_node(thought, html=(pass_me, pass_me), latex=(pass_me, pass_me),
        text=(pass_me, pass_me), man=(pass_me, pass_me))
    app.add_generic_role('thought', thought)
    
    app.add_node(textsc, html=(pass_me, pass_me), latex=(pass_me, pass_me),
        text=(pass_me, pass_me), man=(pass_me, pass_me))
    app.add_generic_role('textsc', textsc)
    
    app.add_builder(SffmsBuilder)

def skip_me(self, node): raise nodes.SkipNode

def pass_me(self, node): pass

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
        outfile = path.join(self.outdir, 'sffms', os_path(self.config.master_doc) + self.out_suffix)
        ensuredir(path.dirname(outfile))
        try:
            f = codecs.open(outfile, 'w', 'utf-8')
            try:
                f.write(self.writer.output)
            finally:
                f.close()
        except (IOError, OSError), err:
            self.warn("error writing file %s: %s" % (outfile, err))
        self.info('done')
        
    def assemble_doctree(self):
        master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set() , master, tree, darkgreen)
        tree['docname'] = master
        
        # skip code that checks references, etc.
        return tree
    
    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding='utf-8')
        output = self.writer.write(doctree, destination)    

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
                setattr(self, 'visit_'+name[0], self.default_skip_handler)
            elif name[1] == 'pass':
                setattr(self, 'visit_'+name[0], self.default_pass_handler)
                setattr(self, 'depart_'+name[0], self.default_pass_handler)
            else:
                raise ValueError("When assigning node handlers, you must set %s to either 'skip' or 'pass'." % name[0])

    def default_pass_handler(self, node): pass

    def default_skip_handler(self, node): raise nodes.SkipNode
    
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
        if papersize and papersize in ['a4paper', 'letterpaper']:
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

class thought(nodes.Inline, nodes.TextElement): pass

class textsc(nodes.Inline, nodes.TextElement): pass

class suppress_numbering(nodes.General, nodes.Element): pass
    
class synopsis(nodes.Structural, nodes.Element): pass

class SffmsSuppressNumberingDirective(Directive):
    
    def run(self):
        return [suppress_numbering('')]

class SffmsSynopsisDirective(Directive):
    
    node_class = synopsis
    has_content = True
    
    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        synopsis_node = self.node_class(rawsource=text)
        self.state.nested_parse(self.content, self.content_offset, synopsis_node)
        return [synopsis_node]
