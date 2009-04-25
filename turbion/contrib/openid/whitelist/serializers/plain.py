mime_types = ['text/plain']

def generator(openids,  buf):
    return buf.write('\n'.join(list(openids)))

def parser(content):
    return content.split('\n')
