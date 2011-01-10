from builders import SffmsBuilder
from addnodes import add_nodes

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
    
    add_nodes(app)
    
    app.add_builder(SffmsBuilder)
