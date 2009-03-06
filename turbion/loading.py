from turbion.core.utils.loading import get_module_attrs, NoModuleError

SUB_APPLICATIONS = (
    "assets", "blogs", "profiles", "utils"
)

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

def indexes():
    for app in SUB_APPLICATIONS:
        try:
            get_module_attrs("turbion.core.%s" % app, "index")
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
