
SUB_APPLICATIONS = (
    "assets", "blogs", "profiles", "staticpages", "utils", "capabilities"
)

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

def connectors():
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            get_module_attrs(app, "connector")
        except NoModuleError:
            pass

def admins():
    for app in SUB_APPLICATIONS:
        try:
            get_module_attrs("turbion.core.%s" % app, "admin")
        except NoModuleError:
            pass

def tests():
    from django.test import TestCase
    test_classes = {}

    for app in SUB_APPLICATIONS:
        try:
            test_classes.update(
                get_module_attrs(
                    "turbion.core.%s" % app,
                    "tests",
                    lambda attr: isinstance(attr, type) and issubclass(attr, TestCase)
                )
            )
        except NoModuleError:
            pass

    return test_classes

def models():
    from django.db.models import Model
    model_classes = {}

    for app in SUB_APPLICATIONS:
        try:
            model_classes.update(
                get_module_attrs(
                    "turbion.core.%s" % app,
                    "models",
                    lambda attr: isinstance(attr, type) and issubclass(attr, Model)
                )
            )
        except NoModuleError:
            pass

    return model_classes

def _load_paths(leaf_module):
    paths = []

    for app in SUB_APPLICATIONS:
        try:
            paths.extend(
                get_module_attrs(
                    "turbion.core.%s" % app,
                    leaf_module
                )["__path__"]
            )
        except NoModuleError:
            pass

    return paths

templatetags = lambda: _load_paths("templatetags")
commands = lambda: _load_paths("management.commands")
