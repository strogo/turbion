# -*- coding: utf-8 -*-
from openid.store.filestore import OpenIDStore

from turbion.openid.models import Association, Nonce

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
        pass

    def cleanupAssociations(self):
        pass
