import os
from unittest import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from smuggler.utils import save_uploaded_file_on_disk


def p(*args):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), *args))


class TestSaveUploadedFileOnDisk(TestCase):
    def test_save_uploaded_file_on_disk(self):
        path = p('..', 'smuggler_fixtures', 'test.json')
        save_uploaded_file_on_disk(
            SimpleUploadedFile('test.json', b'[]'), path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)
