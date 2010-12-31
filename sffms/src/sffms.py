from docutils import nodes, writers
from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path

from sphinx.writers.text import TextWriter

def setup(app):
    
    # Should be one of: submission, novel, anon, baen, daw, wotf, nonsubmission. TODO: validate value.
    app.add_config_value('sffms_submission_type', 'submission', '')

    # Should be one of: smart, dumb, None. TODO: validate value.
    app.add_config_value('sffms_quote_type', None, '')

    # Removes the title page. Only usable when submission type is 'nonsubmission'.
    app.add_config_value('sffms_notitle', False, '')
    app.add_config_value('sffms_courier', False, '')
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
    
    # Set the wordcount manually to some value. Can also set to be empty, to suppress. 
    # Implement with False? None? []? Perhaps the default is True, and the user can set it to be a number or None.
    app.add_config_value('sffms_wordcount', None, '')

    app.add_config_value('sffms_disposable', False, '')
    app.add_config_value('sffms_frenchspacing', False, '')

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
    
    # TODO need to actually instantiate a writer
    def prepare_writing(self, docnames):
        self.writer = SffmsWriter(self)
    
    def get_relative_uri(self, from_, to, typ=None):
        return self.get_target_uri(to, typ)
    
    # LaTeXBuilder has slightly more complicated behavior here, might need to copy wholesale    
    def get_target_uri(self, docname, typ):
        return '%' + docname
    
    # TODO need to actually write something
    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding='utf-8')
        output = self.writer.write(doctree, destination)
        print output
        

# TODO
class SffmsWriter(writers.Writer):
    
    # a writer has a self.output = None, which is then set by calling translate()
    output = None
    
    # a writer has a self.document = None, which is then set by calling write()
    document = None
    
    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder

    # at this point, self.document has been set by write()
    def translate(self):
        translator = SffmsTranslator(self.document, self.builder)
        self.document.walkabout(translator)
        self.output = translator.astext()



class SffmsTranslator(nodes.NodeVisitor):
    
    # a Translator needs a self.body = [] to append to?
    body = []
    
    def __init__(self, document, builder):
        nodes.NodeVisitor.__init__(self, document)
        self.assign_node_handlers()
    
    def assign_node_handlers(self):
        nodenames = [
            ('abbreviation', 'skip'),
            ('acks', 'skip'),
            ('admonition', 'skip'),
            ('attribution', 'skip'),
            ('block_quote', 'skip'),
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
            ('compound', 'skip'),
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
            ('document', 'skip'),
            ('download_reference', 'skip'),
            ('emphasis', 'skip'),
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
            ('line', 'skip'),
            ('line_block', 'skip'),
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
            ('paragraph', 'skip'),
            ('pending_xref', 'skip'),
            ('problematic', 'skip'),
            ('production', 'skip'),
            ('productionlist', 'skip'),
            ('raw', 'skip'),
            ('refcount', 'skip'),
            ('reference', 'skip'),
            ('row', 'skip'),
            ('rubric', 'skip'),
            ('section', 'skip'),
            ('seealso', 'skip'),
            ('start_of_file', 'skip'),
            ('strong', 'skip'),
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
    
    def astext(self):
        return ''.join(self.body)
    
    def visit_Text(self, node):
        self.body.append(node.astext())
        
    def visit_compact_paragraph(self, node):
        pass

    def depart_Text(self, node): pass
