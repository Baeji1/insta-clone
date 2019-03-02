from django.test import TestCase
from .models import UserModel,Post,CommentModel,FollowModel, ActionModel
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class ModelTestCases(TestCase):

	def setUp(self):
		UserModel.objects.create_user(
			username = 'testname1',
			password = 'testpass',
			)
		UserModel.objects.create_user(
			username = 'testname2',
			password = 'testpass',
			profile_name = 'testpname',
			bio = 'test user',
			)
		d = UserModel.objects.get(pk=2)
		Post.objects.create(
			uid = d,			
			post_image = 'insta/defprofpic.png',
			post_caption = 'test post',
			)		

	def test_can_create_user_object(self):
		old_count = UserModel.objects.count()
		UserModel.objects.create(
			username = 'testname',
			password = 'testpass',
			profile_name = 'testpname',
			bio = 'test user',
			)
		new_count = UserModel.objects.count()
		self.assertEqual(new_count,old_count+1)		

	def test_can_create_post_object(self):
		old_count = Post.objects.count()
		z = UserModel.objects.get(username='testname1')
		Post.objects.create(
			uid = z,
			post_image = 'insta/defprofpic.png',
			post_caption = 'test post',
			)						
		new_count = Post.objects.count()
		self.assertEqual(new_count,old_count+1)

	def test_can_comment_on_post(self):
		old_count = CommentModel.objects.count()		
		u = UserModel.objects.get(username='testname2')
		z = Post.objects.get(post_id=1)
		CommentModel.objects.create(
			comment_text = 'test comment',
			c_uid = u,
			c_post_id = z
			)
		new_count = CommentModel.objects.count()
		self.assertEqual(new_count,old_count+1)

	def test_can_follow(self):
		old_count = FollowModel.objects.count()
		FollowModel.objects.create(
			a_username = UserModel.objects.get(username='testname1'),
			b_username = UserModel.objects.get(username='testname2').username
			)
		new_count = FollowModel.objects.count()
		self.assertEqual(new_count,old_count+1)

	def test_user_can_take_action(self):
		old_count = ActionModel.objects.count()
		ActionModel.objects.create(
			uid = UserModel.objects.get(username='testname2'),
			post_id = Post.objects.get(post_id=1),
			action = 1
			)
		new_count = ActionModel.objects.count()
		self.assertEqual(new_count,old_count+1)

	def test_like_function(self):
		old_count = ActionModel.objects.count()		
		u = UserModel.objects.get(username='testname1')		
		p = Post.objects.get(pk=1)
		old_score = p.calculateScore()
		self.assertEqual(u.like(p),'like')		
		new_count = ActionModel.objects.count()
		self.assertEqual(new_count,old_count+1)
		self.assertEqual(p.calculateScore(),old_score+1)

	def test_dislike_function(self):
		old_count = ActionModel.objects.count()		
		u = UserModel.objects.get(username='testname1')
		p = Post.objects.get(pk=1)	
		old_score = p.calculateScore()
		self.assertEqual(u.dislike(p),'dislike')
		new_count = ActionModel.objects.count()
		self.assertEqual(new_count,old_count+1)
		self.assertEqual(p.calculateScore(),old_score-1)

	def test_like_dislike(self):				
		u = UserModel.objects.get(username='testname1')
		g = UserModel.objects.get(username='testname2')
		p = Post.objects.get(pk=1)	
		old_score = p.calculateScore()
		u.like(p)
		u.like(p)
		u.dislike(p)
		new_score = p.calculateScore()
		self.assertEqual(old_score-1,new_score)
		g.like(p)
		self.assertEqual(new_score+1,p.calculateScore())

	def test_user_can_make_post(self):
		u = UserModel.objects.get(username='testname1')
		old_count = Post.objects.count()
		z = u.make_post('insta/defprofpic.png','test status')
		new_count = Post.objects.count()
		assert(z>0)	
		self.assertEqual(new_count,old_count+1)

	def test_user_can_make_comment(self):
		u = UserModel.objects.get(username='testname1')
		p = Post.objects.get(pk=1)
		old_count = CommentModel.objects.count()
		z = u.make_comment(p,'test comment 1',None)
		new_count = CommentModel.objects.count()
		assert(z>0)
		self.assertEqual(new_count,old_count+1) 

	def test_user_can_make_a_comment_on_a_comment(self):
		u = UserModel.objects.get(username='testname1')
		p = Post.objects.get(pk=1)
		old_count = CommentModel.objects.count()
		z = u.make_comment(p,'test comment 1',None)
		new_count = CommentModel.objects.count()
		assert(z>0)
		self.assertEqual(new_count,old_count+1) 
		uu = UserModel.objects.get(username='testname2')
		zz = uu.make_comment(p,'test comment 2',CommentModel.objects.get(pk=z))
		self.assertEqual(CommentModel.objects.count(),new_count+1)
		assert(zz>0)

	def test_can_follow_user(self):
		u = UserModel.objects.get(username='testname1')
		uu = UserModel.objects.get(username='testname2')
		old_count = FollowModel.objects.count()
		self.assertEqual(u.follow_user(uu),True)
		self.assertEqual(uu.follow_user(u),True)
		self.assertEqual(u.follow_user(uu),None)
		new_count = FollowModel.objects.count()
		self.assertEqual(new_count,old_count+2)

	def test_can_get_follow_list(self):
		u = UserModel.objects.get(username='testname1')
		uu = UserModel.objects.get(username='testname2')
		s = UserModel.objects.create(username='test')
		old_count = len(u.get_follow_list())
		u.follow_user(uu)
		u.follow_user(s)
		new_count = len(u.get_follow_list())
		self.assertEqual(new_count,old_count+2)

	def test_can_get_post_list(self):
		u = UserModel.objects.get(username='testname1')
		t = authenticate(username='testname1',password='testpass')
		uu = UserModel.objects.get(username='testname2')
		s = UserModel.objects.create(username='test')
		s.make_post('defprofpic.png','test')
		uu.make_post('defprofpic.png','test')
		u.follow_user(uu)
		u.follow_user(s)
		z = u.get_follow_list()
		self.assertEqual(len(z),2)
		z = u.get_follow_post_list()
		self.assertEqual(len(z),3)

	def test_create_with_user(self):
		u = UserModel.objects.get(username='testname2')		
		t = authenticate(username='testname2',password='testpass')
		z = UserModel.objects.get(user=t)
		print(z,type(z))
		x = UserModel.objects.all()
		print(x,User.objects.all())


"""
class ViewTestCases(TestCase):
	
	def setUp(self):
		Author.objects.create(
			author_name = 'abcd',
			publisher = 'penguin'
		)		
		Book.objects.create(
			book_name = 'testbook',
			book_id = '22ddss',
			author = Author.objects.get(pk=1),			
			genre = 'drama',
			stock = 10
		)
		self.client = APIClient()

	def test_library_can_update_book(self):
		b = Book.objects.all()[0]
		change_stock = {'stock': 30}
		response = self.client.put(
			reverse('library:stocks'),
			change_stock,
		)
		self.assertEqual(response.status_code,status.HTTP_200_OK)

class TemplateTestCases(TestCase):
	
	def setUp(self):
		self.client = APIClient()

	def test_index_page(self):
		response = self.client.get(reverse('library:stocks'))
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertTemplateUsed(response,'library/stocks.html')
"""
