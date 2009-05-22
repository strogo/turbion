# Allow trusted users to skip further antispam checks

def process_form_submit(request, form, child, parent=None):
    return child.created_by.trusted and 'ham'
