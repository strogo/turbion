import time
import base64
from openid.store.filestore import OpenIDStore

from django.db import connection

from turbion.core.openid.models import Association, Nonce

qn = connection.ops.quote_name

class DatabaseStore(OpenIDStore):
    def __init__(self, origin=Association.origins.consumer):
        self.origin = origin

    def get_assocs(self):
        return Association.objects.filter(origin=self.origin)

    def storeAssociation(self, server_url, association):
        assoc = Association.objects.create(
            server_url=server_url,
            handle=association.handle,
            secret=base64.encodestring(association.secret),
            issued=association.issued,
            lifetime=association.lifetime,
            assoc_type=association.assoc_type,
            origin=self.origin
        )

    def getAssociation(self, server_url, handle=None):
        from openid import association
        try:
            if handle:
                assoc = self.get_assocs().get(server_url=server_url, handle=handle)
            else:
                assoc = self.get_assocs().filter(server_url=server_url).order_by("-issued")[0]
            return association.Association(
                     handle=assoc.handle,
                     secret=base64.decodestring(assoc.secret),
                     issued=assoc.issued,
                     lifetime=assoc.lifetime,
                     assoc_type=assoc.assoc_type
            )
        except (Association.DoesNotExist, IndexError), e:
            return None

    def removeAssociation(self, server_url, handle):
        try:
            assoc = self.get_assocs().get(server_url=server_url, handle=handle)
            assoc.delete()
            return True
        except Association.DoesNotExist:
            return False

    def useNonce(self, server_url, timestamp, salt):
        nonce, created = Nonce.objects.get_or_create(
            server_url=server_url,
            timestamp=timestamp,
            salt=salt,
            origin=self.origin,
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
