from builders import SffmsBuilder
from addnodes import add_nodes

def setup(app):
    
    app.add_builder(SffmsBuilder)
    
    # Adds all custom nodes, roles, and directives ('thought', 'synopsis', ...)
    add_nodes(app)
        
    app.add_config_value('sffms_title', None, '')               # REQUIRED. Sets the title.
    app.add_config_value('sffms_author', None, '')              # REQUIRED. Sets the author name.
    app.add_config_value('sffms_nonsubmission', False, '')      # Changes the layout. Opens up the 'notitle' option.
    app.add_config_value('sffms_notitle', False, '')            # Removes the title page if nonsubmission = True.
    app.add_config_value('sffms_novel', False, '')              # Uses chapters, changes to novel layout.
    app.add_config_value('sffms_submission_type', None, '')     # Tweaks the layout. One of: anon, baen, daw, wotf.
    app.add_config_value('sffms_quote_type', None, '')          # Changes quote behavior. One of: smart, dumb.
    app.add_config_value('sffms_courier', False, '')            # Overrides the default monospace font.
    app.add_config_value('sffms_papersize', None, '')           # Changes papersize. One of: a4paper, letterpaper.  
    app.add_config_value('sffms_sceneseparator', None, '')      # Changes the scene separator from "#". 
    app.add_config_value('sffms_thirty', None, '')              # Changes the end-of-story symbol from "# # # # #".  
    app.add_config_value('sffms_msheading', None, '')           # Overrides the running header with arbitrary LaTeX.
    app.add_config_value('sffms_runningtitle', None, '')        # Sets the title in the running header, overriding the title.
    app.add_config_value('sffms_authorname', None, '')          # Sets your real name, if that differs from your nom de plume.
    app.add_config_value('sffms_surname', None, '')             # Sets the name in the running header, overriding the author.
    app.add_config_value('sffms_address', None, '')             # Provides a free-form multi-line address. Use triple quotes.
    app.add_config_value('sffms_wordcount', 'default', '')      # Sets the wordcount manually, or if None, suppresses entirely.
    app.add_config_value('sffms_disposable', False, '')         # Marks the document as disposable.
    app.add_config_value('sffms_frenchspacing', False, '')      # Changes to one space between sentences.
    app.add_config_value('sffms_doublespace_verse', False, '')  # Doublespaces verse instead of single-spacing.
    

