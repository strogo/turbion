from django.template import Parser, Lexer, Context
from django.template.loader_tags import BlockNode

class ProcessingParser(Parser):
    builtin_tags = set(['block'])
    builtin_filters = set([])

    def __init__(self, *args, **kwargs):
        super(ProcessingParser, self).__init__(*args, **kwargs)

        self.tags = dict([(name, tag)\
                for name, tag in self.tags.iteritems() if name in self.builtin_tags])
        self.filters = dict([(name, filter)\
            for name, filter in self.tags.iteritems() if name in self.builtin_filters])

def compile_string(template_string):
    lexer = Lexer(template_string, None)
    parser = ProcessingParser(lexer.tokenize())
    return parser.parse()

def render_string(template_string, context={}):
    return compile_string(template_string).render(Context(context))

def extract_block(template_string, block_name, context={}):
    nodelist = compile_string(template_string)

    blocks = dict([(n.name, n) for n in nodelist.get_nodes_by_type(BlockNode)])

    return blocks[block_name].render(Context(context)).strip('\n ')
