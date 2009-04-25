from django.core.management.base import NoArgsCommand

from turbion.core.watchlist.models import Message

class Command(NoArgsCommand):
    help = 'Performs email watchlist messages sending'

    def handle_noargs(self, **options):
        for message in Message.objects.all():
            try:
                message.send()
            except:
                pass
            message.delete()
