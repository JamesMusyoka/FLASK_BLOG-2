from app.models import Comment,User
from app import db

def setUp(self):
        self.user_James = User(username = 'jamesmuito',password = 'banana', email = 'jamesmu475@gmail.com')
        self.new_comment = Comment(blog_id=123,blog_title='My experience in Moringa School',blog_comment='This is the best way to save my thoughts forever!',user = self.user_Nancy )

def tearDown(self):
        Comment.query.delete()
        User.query.delete()   

def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.movie_id,123)
        self.assertEquals(self.new_blog_title,'My experience in Moringa School')
        self.assertEquals(self.new_review.user,self.user_Nancy)             

def test_save_comment(self):
    self.new_comment.save_comment()
    self.assertTrue(len(Comment.query.all())>0)      

def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_reviews(12345)
        self.assertTrue(len(got_comments) == 1)      