import operator

serializers = []
mime_types_modules = ['_xml', 'json', 'plain']

for mod_name in mime_types_modules:
    mod = __import__('turbion.contrib.openid.whitelist.serializers.%s' % mod_name, {}, {}, [''])

    serializers.append({
        'mime_types': set(getattr(mod, 'mime_types')),
        'parser': getattr(mod, 'parser', None),
        'generator': getattr(mod, 'generator', None)
    })

def _get_handler(name):
    def _handler(mime_type):
        for s in serializers:
            if mime_type in s['mime_types'] and s[name]:
                return s[name], s['mime_types']
        return None, None
    return _handler

get_generator = _get_handler('generator')
get_parser = _get_handler('parser')

def get_accept():
    return reduce(operator.add, [list(s['mime_types']) for s in serializers])
