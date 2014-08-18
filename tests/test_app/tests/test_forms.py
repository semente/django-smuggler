from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from smuggler.forms import ImportFileForm


class TestForm(TestCase):
    def test_requires_file(self):
        form = ImportFileForm({}, {})
        self.assertFalse(form.is_valid())
        self.assertEqual({'file': [u'This field is required.']}, form.errors)

    def test_invalid_file_extension(self):
        f = SimpleUploadedFile('invalid.txt', b'invalid')
        form = ImportFileForm({}, {
            'file': f
        })
        self.assertFalse(form.is_valid())
        self.assertEqual({'file': [u'Invalid file extension.']}, form.errors)

    def test_valid_file_extension(self):
        f = SimpleUploadedFile('valid.json', b'[]')
        form = ImportFileForm({}, {
            'file': f
        })
        self.assertTrue(form.is_valid())
