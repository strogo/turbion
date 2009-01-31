from django import template

register = template.Library()

class IfHasCapNode(template.Node):
    def __init__(self, cap, set, instance, all, nodelist_true, nodelist_false):
        self.cap = cap
        self.set = set
        self.instance = instance
        self.all = all
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfHasCap node>"

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def render(self, context):
        user = context["user"]

        if self.instance:
            instance = self.instance.resolve(context, True)
        else:
            instance = None

        if user.is_authenticated()\
            and user.has_capability(self.cap, self.set, instance, self.all):
            return self.nodelist_true.render(context)

        return self.nodelist_false.render(context)

def create_tag(for_capability=True):
    def if_has_capability(parser, token):
        """
        {% if_has_cap "cap1,cap2" obj %}

        {% else %}

        {% end_if_has_caps %}
        """
        bits = token.contents.split()
        tag_name = bits[0]
        if len(bits) < 2:
            raise template.TemplateSyntaxError("'%s' statement requires at least one argument" % tag_name)

        cap_bits = [perm.strip() for perm in bits[1].split(",")]

        if for_capability:
            cap = cap_bits
            set = None
        else:
            cap = None
            set = cap_bits

        instance = len(bits) == 3 and parser.compile_filter(bits[2]) or None

        nodelist_true = parser.parse(('else', 'end_%s' % tag_name))
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse(('end_%s' % tag_name,))
            parser.delete_first_token()
        else:
            nodelist_false = template.NodeList()

        return IfHasCapNode(cap, set, instance, True, nodelist_true, nodelist_false)
    return if_has_capability

if_has_cap = register.tag(name="if_has_cap")(create_tag(True))
if_has_capset = register.tag(name="if_has_capset")(create_tag(False))
