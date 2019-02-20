import unittest
from app.models import Blog

class UserModelTest(unittest.TestCase):

    def setUp(self):
        '''
        method to run before every test
        '''

        self.new_blog = Blog(123,'My life in Moringa School')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))
