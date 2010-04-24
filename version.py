from subprocess import PIPE, Popen
import re
import os

TIMEZONE_RE = re.compile('(\+\d+)')

def get_output(*cmd):
    return Popen(cmd, stdout=PIPE).communicate()[0]

def get_version(base):
    try:
        rev = get_output(
            'git', 'log', '-n', '1', '--pretty=format:%ai%%h', '--',
            os.path.dirname(__file__)
        )
        base += '~%s' % TIMEZONE_RE.sub('', rev.strip('\n\r\t '))\
                           .replace('-', '')\
                           .replace(':', '')\
                           .replace(' ', '')\
                           .replace('%', ':')
    except OSError:
        pass

    return base
