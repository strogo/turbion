from django.core.management.base import NoArgsCommand

from turbion.core.utils.urlfetch import fetch
from turbion.core.whitelist.models import Source, Identity
from turbion.core.whitelist.serializers import get_accept, get_parser
from turbion import logger

class Command(NoArgsCommand):
    help = 'Update whitelist identities from sources'

    def handle_noargs(self, **options):
        for source in Source.objects.all():
            response = fetch(source.url, headers={'Accept': ', '.join(get_accept())})

            if response.status_code != '200':
                logger.error('Cannot fetch whitelist from %s. Got: %s' % (source.url, response.status_code))
                continue

            source.identities.all().delete()

            parser, mimetype = get_parser(response.headers['content-type'])
            if parser:
                for id in parser(response.content):
                    Identity.objects.create(openid=id, source=source)
