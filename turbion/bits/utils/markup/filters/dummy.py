from turbion.bits.utils.markup.filters import Filter

class Dummy(Filter):
    def is_safe(self):
        return False

    def to_html(self, value):
        return value
