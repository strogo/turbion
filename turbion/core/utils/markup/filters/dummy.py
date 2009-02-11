from turbion.core.utils.markup.filters import Filter

class Dummy(Filter):
    def to_html(self, value):
        return value
