from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.db import connection, IntegrityError

from turbion.bits.profiles.models import Profile

class Command(NoArgsCommand):
    help = 'Revolve (executes) all needed gears once'

    option_list = NoArgsCommand.option_list + (
        make_option('--dry', action='store_true', default=False,
            help='Dry run. Make no changes'),
        make_option('--fields', action='store', default="username,email",
            help='Key field names')
    )

    def handle_noargs(self, dry=False, fields="username,email", **options):
        fields = fields.split(",")

        for clone_meta in self.get_clone_profiles(fields):
            lookup = dict([(field, clone_meta[i]) for i, field in enumerate(fields)])

            clones = Profile.objects.filter(**lookup).order_by("-email", "-date_joined")

            base_obj, others = clones[0], clones[1:]

            print u"Base object %s" % base_obj

            for obj in others:
                for rel, model in Profile._meta.get_all_related_objects_with_model():
                    if model is not None:
                        continue

                    name = rel.field.name

                    related_model = rel.model

                    for related_object in related_model._default_manager.filter(**{name: obj}):
                        setattr(related_object, name, base_obj)

                        print u"\t\tSaving %s - %s with reassigned profile" % (related_model._meta.object_name,
related_object.pk,)
                        if not dry:
                            try:
                            	related_object.save()
                            except IntegrityError:
                                pass

                print u"\tDeleting %s" % obj
                if not dry:
                    obj.delete()

    def get_clone_profiles(self, fields):
        fields = map(connection.ops.quote_name, fields)
        not_nulls = " AND ".join(['%(f)s IS NOT NULL AND %(f)s != ""' % {'f': field} for field in fields])

        query = """SELECT DISTINCT
			%(fields)s, COUNT(*) AS count
                   FROM
                        turbion_profile p
                   JOIN
                        auth_user u ON u.id=p.user_ptr_id
                   WHERE
                        trusted=0 AND %(not_nulls)s
                   GROUP BY
                        %(fields)s
                   HAVING
                        count > 1;""" % {'fields': ",".join(fields), 'not_nulls': not_nulls}

        cursor = connection.cursor()

        cursor.execute(query)

        return cursor
