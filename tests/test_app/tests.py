import StringIO
from django.test import TestCase
from smuggler import utils


class BasicDumpTestCase(TestCase):
    def test_serialize_to_response(self):
        response = StringIO.StringIO()
        utils.serialize_to_response(response=response)
        self.assertEqual('[]', response.getvalue())


