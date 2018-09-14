"""Doc."""
import os
from google.cloud import datastore, storage


project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
dc = datastore.Client(project_id)
sc = storage.Client(project_id)

STORAGE_FOLDER = 'gs://{}-media'.format(project_id)
S = '-'

bucket = sc.get_bucket(STORAGE_FOLDER)


class FileStore:
    """Doc."""

    def save(self, user_id, file_id, file):
        """Doc."""
        path = self.get_path(user_id, file_id)
        blob = bucket.blob(path)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        # file.save(path)

    def get_path(self, user_id, file_id):
        """Doc."""
        li = [str(user_id), str(file_id)]
        return S.join(li)


class DocStore:
    """Doc."""

    def _key(self, user_id, doc_id):
        return dc.key(str(user_id), doc_id)

    def put(self, user_id, doc_id, doc):
        """Doc."""
        print('put', doc)
        entity = datastore.Entity(self._key(user_id, doc_id))        
        entity.update(doc)
        dc.put(entity)

    def get(self, user_id, doc_id):
        """Doc."""
        r = dc.get(self._key(user_id, doc_id))
        if r is None:
            return r
        doc = {}
        for k, v in r.items():
            doc[k] = v
        print('get', doc)
        return doc

    def delete(self, user_id, doc_id):
        """Doc."""
        return dc.delete(self._key(user_id, doc_id))
