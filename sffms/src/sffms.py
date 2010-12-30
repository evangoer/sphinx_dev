"""Builder for sffms-style LaTeX."""

from docutils import nodes

def setup(app):
	
	app.add_config_value('sffms_activate', False, False)