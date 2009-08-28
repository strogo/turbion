from django.core.management.base import NoArgsCommand, CommandError
from django.core.management.commands import dumpdata
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers

from turbion import models as tm

MODEL_QUEUE = [
    User,
    tm.Profile,
    tm.Tag,
    tm.Post,
    tm.Comment,
    tm.Pingback,
    tm.Feedback,
    tm.Event,
    tm.Subscription,
    tm.Alias,
    tm.Trust,
    tm.Message,
    tm.Source,
    tm.Identity
]

class Command(NoArgsCommand):
    help = 'Dumps blog content'

    option_list = dumpdata.Command.option_list[:-1]

    def handle_noargs(self, **options):
        format = options.get('format', 'json')
        indent = options.get('indent', None)
        show_traceback = options.get('traceback', False)

        def objects():
            for model in MODEL_QUEUE:
                if not model._meta.proxy:
                    for o in model._default_manager.all():
                        yield o

        try:
            return serializers.serialize(format, objects(), indent=indent)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)
