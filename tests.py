from app import app
import unittest
import os

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		app.config['MONGODB_SETTINGS'] = {
			'host': os.environ.get('MONGOLAB_URI') or 'mongodb://localhost/vocabulary',
			'db': 'vocabulary'
		}
		app.config['TESTING'] = True
		self.app = app.test_client()

	def test_register(self):
		resp = self.app.get('/register')
		self.assertEqual(resp.status_code, 200)

	def test_signin(self):
		resp = self.app.get('/signin')
		self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
	unittest.main()
