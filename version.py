import os

def get_revision(path=None):
    if path is None:
        path = os.path.dirname(os.path.abspath(__file__))

    try:
        from mercurial import hg, ui, repo, node

        try:
            RepoError = repo.RepoError
        except AttributeError:
            RepoError = repo.error.RepoError

        try:
            repository = hg.repository(ui.ui(), path)
        except RepoError:
            return None

        tip = repository.changelog.tip()
        tip_tag = repository.tagslist()[-1][0]

        return (
            repository.changelog.nodemap[tip],
            node.short(tip),
            tip_tag
        )
    except ImportError:
        return None

def get_version(path=None):
    rev = get_revision(path)
    if rev is None:
        raise RuntimeError('Cannot determine version')
    return "hg%s" % rev[0]

def write_version(path=None, filename='VERSION', source=None):
    try:
        version = get_version(path)
    except RuntimeError:
        pass

    outp = file(filename, 'w')
    outp.write(version)
    outp.close()

def read_version(filename='VERSION'):
    return file(filename).read()