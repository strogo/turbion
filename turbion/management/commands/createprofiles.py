from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import connection, IntegrityError
from django.contrib.auth.models import User

from turbion.core.profiles.models import Profile

class Command(NoArgsCommand):
    help = 'Create profiles for raw django users'

    option_list = NoArgsCommand.option_list + (
        make_option('--dry', action='store_true', default=False,
            help='Dry run. Make no changes'),
    )

    def handle_noargs(self, dry=False, **options):
        for user in User.objects.all():
            try:
                user.profile
            except Profile.DoesNotExist:
                print "Creating profile for `%s`" % user
                if not dry:
                    user.save() # assume that post_save signal handler is set
