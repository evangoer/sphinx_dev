from docutils import nodes, writers
from sphinx.builders import Builder

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