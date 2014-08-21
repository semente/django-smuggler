import os
from unittest import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from smuggler.utils import get_file_list, save_uploaded_file_on_disk

p = lambda *args: os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               *args))


class TestGetFileList(TestCase):
    def test_get_file_list(self):
        file_list = get_file_list(p('..', 'smuggler_fixtures'))
        self.assertEqual([('page_dump.json', '0.1 KB')], file_list)


class TestSaveUploadedFileOnDisk(TestCase):
    def test_save_uploaded_file_on_disk(self):
        path = p('..', 'smuggler_fixtures', 'test.json')
        save_uploaded_file_on_disk(
            SimpleUploadedFile('test.json', b'[]'), path)
        self.assertTrue(os.path.exists(path))
        os.unlink(path)
