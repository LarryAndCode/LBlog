from flaskext.markdown import Markdown

def init_templatefilter(app):

    @app.template_filter('cutwords')
    def reverse_filter(s):
        return s[:100]

    Markdown(app,
            extensions=['footnotes'],
            entension_configs={'footnotes': ('PLACE_MARKER', '```')},
            safe_mode=True,
            output_format='html4')
