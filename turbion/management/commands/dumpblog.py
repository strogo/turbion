from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.core.management.commands import dumpdata
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import get_app, get_model, get_models

from turbion.models import *

MODEL_QUEUE = [
    User,
    Profile,
    Tag,
    Post,
    Comment,
    Pingback,
    Feedback,
    Event,
    Subscription,
    Alias,
    Trust,
    Message,
    Source,
    Identity
]

class Command(NoArgsCommand):
    help = 'Dumps blog content'

    option_list = list(dumpdata.Command.option_list[:-1]) + [
        make_option('-a', '--add', dest='add', action='append', default=[],
            help='Model (appname.modelname) or app name to include into dump (use multiple --add to include multiple models).')
    ]

    def handle_noargs(self, **options):
        format = options.get('format', 'json')
        indent = options.get('indent', None)
        show_traceback = options.get('traceback', False)
        add = options.get('add', [])
        
        models = MODEL_QUEUE[:]
        for app_label in add:
            if '.' in app_label:
                app_label, model_label = app_label.split('.', 1)
                try:
                    get_app(app_label)
                except ImproperlyConfigured:
                    raise CommandError("Unknown application: %s" % app_label)
                
                model = get_model(app_label, model_label)
                
                if model is None:
                    raise CommandError("Unknown model: %s.%s" % (app_label, model_label))
                
                models.append(model)
            else:
                try:
                    app = get_app(app_label)
                except ImproperlyConfigured:
                    raise CommandError("Unknown application: %s" % app_label)
                models.extend(get_models(app))

        def objects():
            for model in models:
                if not model._meta.proxy:
                    for o in model._default_manager.all():
                        yield o

        try:
            return serializers.serialize(format, objects(), indent=indent)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)
