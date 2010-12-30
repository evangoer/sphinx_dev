from docutils import nodes, writers
from sphinx.builders import Builder

def setup(app):
	
	# TODO currently ignored
	app.add_config_value('sffms_activate', False, '')
	app.add_config_value('sffms_frenchspacing', True, '')

	app.add_builder(SffmsBuilder)
	
class SffmsBuilder(Builder):
	"""
	Builder for sffms-style LaTeX. Totally different output
	from the default Sphinx LaTeX builder.
	"""
	
	name = "sffms"
	format = "latex"
	
	# Could copy image list from LaTeXBuilder. But for now, images aren't supported.
	supported_image_types = []  
	
	# TODO grab initial sffms configuration
	def init(self):
		pass
	
	def get_outdated_docs(self):
		return 'all documents'
	
	# TODO need to actually instantiate a writer
	def prepare_writing(self, docnames):
		pass
	
	def get_relative_uri(self, from_, to, typ=None):
		return self.get_target_uri(to, typ)
	
	# LaTeXBuilder has slightly more complicated behavior here, might need to copy wholesale	
	def get_target_uri(self, docname, typ):
		return '%' + docname
	
	# TODO need to actually write something
	def write_doc(self, docname, doctree):
		print "IM IN UR DOCNAME! IM WRITIN UR DOC! (%s)" % docname
		print "Frenchspacing is set to %r" % self.config.sffms_frenchspacing

# TODO
class SffmsWriter(writers.Writer): pass