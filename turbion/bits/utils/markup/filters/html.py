from turbion.core.utils.markup.filters import Filter

class Html(Filter):
    def is_safe(self):
        return False
    
    def to_html(self, value):
        return value
