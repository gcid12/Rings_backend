from flask import Flask
from flask.ext.testing import TestCase

class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_post_a(self):
        rv = self.app.post('/moma/',
                            data={"RingName":"Tigers4Adoption",
                                  "RingVersion":2,
                                  "FieldName_1":"Name",
                                  "FieldLabel_1":"Name of the tiger"})

        print('hello from the test')

        assert 'Ring' in rv.data


