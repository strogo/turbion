# Allow trusted users to skip further antispam checks
from turbion.bits.antispam import Filter

class Trusted(Filter):
    def process_form_submit(self, request, form, child, parent=None):
        return child.created_by.trusted and 'ham'
