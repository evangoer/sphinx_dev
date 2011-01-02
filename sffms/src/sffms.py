from docutils import nodes, writers
from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees

from sphinx.writers.text import TextWriter

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
    
    app.add_config_value('sffms_address', None, '')

    app.add_config_value('sffms_authorname', None, '')
    app.add_config_value('sffms_surname', None, '')
    
    # In sffms, this is a free-form multi-line piece of text. Need to think how to specify it. Triple quotes?
    app.add_config_value('sffms_address', None, '')
    
    # Set the wordcount manually to some value. Can also set to be empty, to suppress. 
    # Implement with False? None? []? Perhaps the default is True, and the user can set it to be a number or None.
    app.add_config_value('sffms_wordcount', None, '')

    app.add_config_value('sffms_disposable', False, '')
    app.add_config_value('sffms_frenchspacing', False, '')


    app.add_generic_role('thought', thought)
    app.add_generic_role('textsc', textsc)
    
    app.add_builder(SffmsBuilder)

# custom inline styles from sffms: thought and textsc
#
# TODO: Danger Will Robinson! Adding these custom roles means
# we are screwing up all the other builds. How do we patch up
# the other builders?
class thought(nodes.Inline, nodes.TextElement): pass

class textsc(nodes.Inline, nodes.TextElement): pass

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
    
    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.header = SffmsHeader(config)
        self.assign_node_handlers()

    def astext(self):
        return ''.join(self.body)
    
    def visit_Text(self, node):
        self.body.append(node.astext())
    
    def depart_Text(self, node): pass
        
    def visit_paragraph(self, node):
        self.body.append('\n')
        
    def depart_paragraph(self, node):
        self.body.append('\n')
    
    # Here is where we need to figure out \newscene, \chapter, and titles.    
    def visit_section(self, node): pass
    
    def depart_section(self, node): pass
    
    def visit_document(self, node):
        self.body.append(self.header.astext())
        self.body.append('\n\\begin{document}\n')
    
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
        self.body.append('\n\\begin{verse}')
        
    def depart_line_block(self, node):
        self.body.append('\n\end{verse}\n')
    
    # TODO: This code is broken -- it inserts '\\' in the wrong places which
    # causes latex to fail. Fix this.
    def visit_line(self, node):
        self.body.append('\\\\\n')
    
    def depart_line(self, node):
        pass
        
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
            ('system_message', 'skip'),
            ('table', 'skip'),
            ('tabular_col_spec', 'skip'),
            ('target', 'skip'),
            ('tbody', 'skip'),
            ('term', 'skip'),
            ('tgroup', 'skip'),
            ('thead', 'skip'),
            ('title', 'pass'),
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
    
    header = []
    
    def __init__(self, config):
        self.config = config
    
    def astext(self):
        self.set_documentclass()
        self.set_title()
        self.set_author()
        self.set_frenchspacing()
        self.header.append('\n')
        return '\n'.join(self.header)
    
    # Handles all options [x,y,z] set for the document class. Output resembles:
    # \documentclass[novel,baen]{sffms}
    def set_documentclass(self):
        options = []
        options_str = ''

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
        
        if len(options) > 0:
            options_str = '[' + ','.join(options) + ']'
           
        self.header.append('\\documentclass' + options_str + '{sffms}')

    def set_title(self):
        if self.config.sffms_title: # TODO and title is a string!
            self.header.append('\\author{' + self.config.sffms_title + '}')
        else:
            raise ValueError("You must provide a non-empty sffms_title.")

    def set_author(self):
        if self.config.sffms_author: # TODO and title is a string!
            self.header.append('\\title{' + self.config.sffms_author + '}')
        else:
            raise ValueError("You must provide a non-empty sffms_author.")
    

        
    def set_frenchspacing(self):
        if self.config.sffms_frenchspacing:
            self.header.append('\\frenchspacing')
    
    