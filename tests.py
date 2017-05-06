import os
import app
import unittest
import tempfile

class RRTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
		app.app.config['TESTING'] = True
		self.app = app.app.test_client()
		with app.app.app_context():
			app.database.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(app.app.config['DATABASE'])

	def test_index(self):
		rv = self.app.get('/')
		assert 'Sign In' in rv.data

if __name__ == '__main__':
	unittest.main()
