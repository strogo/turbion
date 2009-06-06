from django.core.management.base import NoArgsCommand
from django.conf import settings

from turbion.models import Message

class Command(NoArgsCommand):
    help = 'Performs email watchlist messages sending'

    def handle_noargs(self, **options):
        for message in Message.objects.all():
            if message.send()\
                or message.attempt >= settings.TURBION_NOTIFICATION_ATTEMPTS:
                message.delete()
