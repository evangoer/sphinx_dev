from docutils import nodes, writers
from sphinx.builders import Builder
from 

def setup(app):
	
	# TODO currently ignored
	app.add_config_value('sffms_activate', False, False)

	app.add_builder(SffmsBuilder)
	
class SffmsBuilder(Builder):
	"""
	Builder for sffms-style LaTeX. Totally different output
	from the default Sphinx LaTeX builder.
	"""
	
	name = "sffms"
	format = "latex"
	
	# Grab initial configuration
	def init(self):
		pass
	
	def get_outdated_docs(self):
		return 'all documents'
	
	# TODO need to actually instantiate a writer
	def prepare_writing(self, docnames):
		pass
	
	# TODO need to actually write something
	def write_doc(self, docname, doctree):
		print "IM IN UR BUILDER! IM WRITIN UR DOC!"

# TODO
class SffmsWriter(writers.Writer): pass