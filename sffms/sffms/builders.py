import codecs
from os import path
from docutils.io import StringOutput

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees

from sffms.writers import SffmsWriter
from sffms.quickstart.templates import makefile_sffms

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
        self.info('done')
        self.info()
        self.info(bold('writing... '), nonl=True)
        self.write_doc(self.config.master_doc, doctree)
        outfile = path.join(self.outdir, os_path(self.config.master_doc) + self.out_suffix)
        ensuredir(path.dirname(outfile))
        self.write_file(outfile, self.writer.output)
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
    
    def finish(self):
        self.info(bold('copying Makefile... '), nonl=True)
        outfile = path.join(self.outdir, 'Makefile')
        self.write_file(outfile, makefile_sffms)
        self.info('done')
    
    def write_file(self, outfile, content):
        try:
            f = codecs.open(outfile, 'w', 'utf-8')
            try:
                f.write(content)
            finally:
                f.close()
        except (IOError, OSError), err:
            self.warn("error writing file %s: %s" % (outfile, err))
        