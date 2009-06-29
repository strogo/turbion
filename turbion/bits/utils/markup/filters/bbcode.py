from turbion.core.utils.markup.filters import Filter

class Bbcode(Filter):
    def to_html(self, value):
        from postmarkup import render_bbcode
        return render_bbcode(value)
