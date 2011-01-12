from sphinx.util.compat import Directive
from docutils import nodes

def add_nodes(app):    
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

def skip_me(node): raise nodes.SkipNode

def pass_me(node): pass

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