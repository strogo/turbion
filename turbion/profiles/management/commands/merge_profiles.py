# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.db import connection

from turbion.profiles.models import Profile

class Command(NoArgsCommand):
    help = 'Revolve (executes) all needed gears once'

    option_list = NoArgsCommand.option_list + (
        make_option('--dry', action='store_true', default=False,
            help='Dry run. Make no changes'),
        make_option('--except_email', action='store_true', default=False,
            help='Dry run. Make no changes')
    )

    def handle_noargs(self, **options):
        dry = options["dry"]
        except_email = options["except_email"]

        for clone_meta in self.get_clone_profiles(except_email):
            clones = Porofile.objects.filter(
                                        nickname=clone_meta[0],
                                        email=clone_meta[1]
                                    ).sort_by("-email")

            base_obj, others = clones[0], clones[:1]

            print "Base object %s" % base_obj

            for obj in others:
                for rel, model in Profile._meta.get_all_related_objects_with_model():
                    if model is not None:
                        continue

                    name = r.field.name

                    related_model = r.model

                    for related_object in related_name._default_manager.filter(**{name: obj}):
                        setattr(related_object, name, base_obj)

                        print "\t\tSaving %s" % related_object
                        if not dry:
                            related_object.save()

                print "\tDeleting %s" % obj
                if not dry:
                    obj.delete()

    def get_clone_profiles(self, except_email):
        email_str = ", email"
        if except_email:
            email_str = ""

        query = """SELECT DISTINCT
                        nickname%s, COUNT(*) AS count
                   FROM
                        turbion_profile AS p
                   JOIN
                        auth_user AS u ON u.id=p.user_ptr_id
                   WHERE
                        is_confirmed=0
                   GROUP BY
                        nickname%s
                   HAVING
                        count > 1;""" % (email_str, email_str)

        cursor = connection.cursor()

        cursor.execute(query)

        return cursor
