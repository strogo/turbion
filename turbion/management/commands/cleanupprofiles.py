from datetime import datetime, timedelta

from django.core.management.base import NoArgsCommand, CommandError

from turbion.models import Profile, Comment

class Command(NoArgsCommand):
    help = 'Cleans up outdated profiles'
    
    def handle_noargs(self, **options):
        timeout = datetime.now() - timedelta(days=7)
        
        for p in Profile.objects.filter(trusted=False)\
                           .filter(
                              Comment.spams.get_lookup('comments__'),
                              comments__created_on__lt=timeout
                        ):
            p.delete()

    
