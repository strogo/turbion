# -*- coding: utf-8 -*-
import time
from openid.store.filestore import OpenIDStore

from django.db import connection

from turbion.openid.models import Association, Nonce

qn = connection.opts.quote_name

class DatabaseStore(OpenIDStore):
    def storeAssociation(self, server_url, association):
        assoc = Association.objects.create(
            server_url=server_url,
            handle=association.handle,
            secret=association.secret,
            issued=association.issued,
            lifetime=association.lifetime,
            assoc_type=association.assoc_type
        )

    def getAssociation(self, server_url, handle=None):
        try:
            if handle:
                return Association.objects.get(server_url=server_url, handle=handle)
            else:
                return Association.objects.filter(server_url=server_url).order_by("-issued")[0]
        except (Association.DoesNotExist, IndexError):
            return None

    def removeAssociation(self, server_url, handle):
        try:
            assoc = Association.objects.get(server_url=server_url, handle=handle)
            assoc.delete()
            return True
        except Association.DoesNotExist:
            return False

    def useNonce(self, server_url, timestamp, salt):
        nonce, created = Nonce.objects.get_or_create(
            server_url=server_url,
            timestamp=timestamp,
            salt=salt,
        )

        return created

    def cleanupNonces(self):
        query = "DELETE FROM %s WHERE timestamp < %s" % \
                    (qn(Nonce._meta.db_table), int(time.time()) - nonce.SKEW)
        cursor = connection.cursor()

        cursor.execute(query)

        return cursor.rowcount

    def cleanupAssociations(self):
        query = "DELETE FROM %s WHERE issued + lifetime < %s" % \
                            (qn(Association._meta.db_table), int(time.time()))
        cursor = connection.cursor()

        cursor.execute(query)

        return cursor.rowcount
