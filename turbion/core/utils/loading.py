class NoModuleError(Exception):
    """
    Custom exception class indicates that given module does not exit at all
    """
    pass

def get_module_attrs(app, module_name, filter=lambda attr: True):
    import imp
    try:
        app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
    except AttributeError:
        raise NoModuleError("Cannot load app `%s`" % app)

    try:
        imp.find_module(module_name, app_path)
    except ImportError:
        raise NoModuleError("Cannot find module `%s` in app `%s`" % (module_name, app))

    mod = getattr(__import__(app, {}, {}, [module_name]), module_name)

    try:
        attrs = mod.__all__
    except AttributeError:
        attrs = dir(mod)

    return dict([(name, getattr(mod, name)) for name in attrs if filter(getattr(mod, name))])
