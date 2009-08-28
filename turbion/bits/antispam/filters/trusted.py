# Allow trusted users to skip further antispam checks
from turbion.bits.antispam import Filter, StopChecking

class Trusted(Filter):
    def process_form_submit(self, request, form, child, parent=None):
        if child.created_by.trusted:
            raise StopChecking
