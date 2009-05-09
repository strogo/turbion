import logging
import os
import operator

VERSION = (0, 8, 2, 'Pushkin', '0')

def get_revision(path=None, check_changes=False):
    if not path:
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    try:
        from mercurial import hg, ui, repo

        try:
            repository = hg.repository(ui.ui(), path)
        except repo.RepoError:
            return None

        tip = repository.changelog.tip()
        tip_tag = repository.tagslist()[-1][0]

        if check_changes and bool(reduce(operator.add, repository.status()[:4])):
            raise RuntimeError('Repository has local modifications')

        return (
            repository.changelog.nodemap[tip],
            hg.short(tip),
            tip_tag
        )
    except ImportError:
        return None

def get_version(bits=4, revision=False):
    base = reduce(
        lambda l, r: (isinstance(r, basestring) and ' ' or '.').join(map(str, [l, r])),
        VERSION[:bits]
    )
    if revision:
        rev = get_revision()
        if rev:
            base += " HG-%s:%s:%s" % rev

    return base

logger = logging.getLogger('turbion')
