from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.datastructures import MultiValueDict
from smuggler.forms import ImportForm


class TestForm(TestCase):
    def test_requires_file(self):
        form = ImportForm({}, {})
        self.assertFalse(form.is_valid())
        self.assertEqual({'uploads': ["This field is required."]},
                         form.errors)

    def test_invalid_file_extension(self):
        f = SimpleUploadedFile('invalid.txt', b'invalid')
        form = ImportForm({}, {
            'uploads': f
        })
        self.assertFalse(form.is_valid())
        self.assertEqual({'uploads': ["Invalid file extension: .txt."]},
                         form.errors)

    def test_valid_file_extension(self):
        f = SimpleUploadedFile('valid.json', b'[]')
        form = ImportForm({}, {
            'uploads': f
        })
        self.assertTrue(form.is_valid())

    def test_valid_uppercase_file_extension(self):
        f = SimpleUploadedFile('valid.JSON', b'[]')
        form = ImportForm({}, {
            'uploads': f
        })
        self.assertTrue(form.is_valid())

    def test_mix_valid_and_invalid(self):
        form = ImportForm({}, MultiValueDict({
            'uploads': [
                SimpleUploadedFile('valid.json', b'[]'),
                SimpleUploadedFile('invalid.txt', b'invalid')
            ]
        }))
        self.assertFalse(form.is_valid())
        self.assertEqual({'uploads': ["Invalid file extension: .txt."]},
                         form.errors)
