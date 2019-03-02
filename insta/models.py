from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# a user object
class UserModel(User):
	#username: string
	#password: string
	#email: email type
	#is_superuser: boolean
	#date_joined: current when created
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	uid = models.BigAutoField(primary_key=True)
	profile_name = models.CharField(max_length=200,blank=False)
	profile_image = models.ImageField(upload_to='insta/',default='insta/defprofpic.png')
	bio = models.CharField(max_length=500, blank=True)
	score = models.IntegerField(default=0)
	followers = models.IntegerField(default=0)
	following = models.IntegerField(default=0)
	count = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	#level = models.CharField(default="Entry Level", max_length=200)

	def __str__(self):
		return self.username

	def get_id(self):
		return self.uid

	def calculateScore(self):
		try:
			x = Post.objects.filter(uid=self)
			for i in x:
				i.calculateScore()
				self.score += i.post_score
			return True
		except:
			return False

	def calculateFollow(self):
		x = FollowModel.objects.filter(a_username=self)
		self.following = x.count()
		x = FollowModel.objects.filter(b_username=self.uid)
		self.followers = x.count()

	def like(self,p):
		if isinstance(p,Post)==False:
			return None		
		flag = False
		try:
			a = ActionModel.objects.get(uid=self,post_id=p)
			print(a.action)
			if a.action == 1:
				a.action = 0
			else:
				a.action = 1
				flag = 'like'
			a.save()
			p.calculateScore()
			return flag
		except:			
			ActionModel.objects.create(
			uid = self,
			post_id = p,
			action = 1
			)
			p.calculateScore()
			flag = 'like'
			return flag
		
		return False

	def dislike(self,p):
		if isinstance(p,Post)==False:
			return None		
		flag = False
		try:
			a = ActionModel.objects.get(uid=self,post_id=p)
			print(a.action)
			if a.action == -1:
				a.action = 0
			else:
				a.action = -1
				flag = 'dislike'
			a.save()
			p.calculateScore()
			return flag
		except:			
			ActionModel.objects.create(
			uid = self,
			post_id = p,
			action = -1
			)
			flag = 'dislike'
			p.calculateScore()
			return flag
		
		return False

	def make_post(self,image_path,image_caption):
		try:
			x = Post.objects.create(
			uid = self,
			post_image = image_path,
			post_caption = image_caption
			)
			return x.post_id
		except:
			return False

	def make_comment(self,c_post,c_text,c_parent):
		try:
			x = CommentModel.objects.create(
				comment_text = c_text,
				c_uid = self,
				c_post_id = c_post,
				c_parent_id = c_parent
				)
			return x.comment_id
		except:
			return False

	def follow_user(self,b_user):
		try:
			x = FollowModel.objects.get(a_username=self,b_username=b_user.get_id())
			return None
		except:
			x = FollowModel.objects.create(
				a_username = self,
				b_username = b_user.get_id()
				)
			return True
		return False

	def unfollow_user(self,b_user):
		try:
			x = FollowModel.objects.get(a_username=self,b_username=b_user.get_id())
			x.delete()
			return True
		except:
			return False

	def get_follow_list(self):
		try:
			x = FollowModel.objects.filter(a_username=self)
			follow_list = []
			for i in x:
				try:
					follow_list.append(UserModel.objects.get(uid=i.b_username))
				except:
					continue
				print('yes')
			return follow_list
		except:
			return False

	def get_follow_post_list(self):
		a = self.get_follow_list()
		if(a==False):
			return a
		for i in a:			
			try:
				post_list = Post.objects.filter(uid__in=a).order_by('-post_time')
				return post_list
			except:
				return False

	def is_follow(self,v_uid):
		try:
			x = FollowModel.objects.get(a_username=self,b_username=v_uid)
			return True
		except:
			return False

	def number_posts(self,uid):
		try:
			x = Post.objects.filter(uid=uid)			
			self.count = len(x)
			print(self.count)
			self.save()
			return self.count
		except:
			self.count = 0
			return 0

	def number_likes(self,uid):
		try:
			self.likes = 0
			x = ActionModel.objects.filter(uid=uid)			
			for i in x:
				if i.action==1:
					self.likes += 1
			print(self.likes)
			self.save()
			return self.likes
		except:
			self.likes = 0
			return 0

	def get_ordered_like(self):
		try:
			for i in UserModel.objects.all():
				i.number_likes(i.uid)
			x = UserModel.objects.order_by('-likes')
			return x
		except:
			return False

	def get_ordered_post(self):
		try:
			for i in UserModel.objects.all():
				i.number_posts(i.uid)
			x = UserModel.objects.order_by('-count')
			return x
		except:
			return False


# a post made by a user
class Post(models.Model):
	post_time = models.DateTimeField(default=timezone.now,blank=False)
	post_id = models.BigAutoField(primary_key=True)
	uid = models.ForeignKey(UserModel, on_delete=models.CASCADE) # needs to be a user 
	post_image = models.ImageField(upload_to='insta/',default=None,blank=False)
	post_caption = models.CharField(max_length=200,blank=True)
	post_score = models.IntegerField(default=0)	
	#likes = models.IntegerField(default=0)
	#dislikes = models.IntegerField(default=0)

	def __str__(self):
		return self.uid.username

	def remove_post(self):
		try:
			self.delete()
			return True
		except:
			return False

	def calculateScore(self):
		try:
			self.post_score = 0
			z = ActionModel.objects.filter(post_id=self)
			for i in z:
				self.post_score += i.action
			return self.post_score
		except:
			return self.post_score

	def get_comments(self):
		try:			
			x = CommentModel.objects.filter(c_post_id=self)
			return x
		except:
			return False


# action taken by a user for a post
class ActionModel(models.Model):
	uid = models.ForeignKey(UserModel, on_delete=models.CASCADE) # needs to be a user
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE) # needs to be a post 
	action = models.IntegerField(default=0)


# user ids of followers-following
class FollowModel(models.Model):
	a_username = models.ForeignKey(UserModel, on_delete=models.CASCADE) # needs to be a user 
	b_username = models.CharField(max_length=200)
	
# a comment made by a user
class CommentModel(models.Model):
	comment_id = models.BigAutoField(primary_key=True)
	comment_text = models.CharField(max_length=255,blank=False)
	comment_score = models.IntegerField(default=0)
	c_uid = models.ForeignKey(UserModel, on_delete=models.CASCADE) # needs to be a user
	c_post_id = models.ForeignKey(Post, on_delete=models.CASCADE) # needs to be a post
	c_parent_id = models.ForeignKey("CommentModel", on_delete=models.CASCADE, blank = True, null=True) # needs to be a comment

