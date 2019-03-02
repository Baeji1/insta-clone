from django.shortcuts import render
from .models import UserModel, Post, FollowModel, ActionModel, CommentModel
from django.views.generic import CreateView
from insta.models import User
from insta.forms import LoginForm,SignupForm,ImageForm,PostForm,BioForm,ProfileForm
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	return render(request, 'insta/index.html', {})

def logout_view(request):
	print('elouol')
	logout(request)
	return redirect('insta:index')

def login_view(request):
	logout(request)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():			
			password = form.cleaned_data['password']
			username = form.cleaned_data['username']
			u = authenticate(request,username=username,password=password)			
			if(u==None):
				return render(request, 'insta/login.html', {
					'form':form,
					'error':'Invalid username or password'
				})
			print(u)
			print(login(request,u),u.id)
			u = UserModel.objects.get(user=u)
			print(u)
			request.session.set_expiry(86400)
			request.session['uid'] = u.uid
			return HttpResponseRedirect(reverse('insta:profile',args=(u.uid,)))
	else:
		form = LoginForm()
	return render(request, 'insta/login.html', {'form':form})

@login_required
def profile(request,uid):
	if request.session['uid']==uid:
		u = UserModel.objects.get(uid=uid)
		u.calculateFollow()
		u.calculateScore()
		a = Post.objects.filter(uid = u).order_by('-post_time')	
		for i in a:
			i.calculateScore()	
		return render(request, 'insta/profile.html', {
			'user':u,			
			'allPosts':a,
			'session_id':uid,
			'session_user':UserModel.objects.get(uid=uid),
		})
	else:
		logout(request)
		return redirect('insta:index')

@login_required
def liking_disliking(request,uid, post_id):
	if request.session['uid']==uid:
		u = UserModel.objects.get(uid=uid)
		p = Post.objects.get(post_id=post_id)
		p.calculateScore()
		flag = None
		owner = None
		if p.uid == u:
			owner = True
		try:
			a = ActionModel.objects.get(uid=uid,post_id=post_id)
			if a.action == 1:
				flag = 'like'
			if a.action == -1:
				flag = 'dislike'
		except:
			pass
		if request.method == 'POST':
			print(request.POST)
			try:
				comment = request.POST['comment']
				if(len(comment))>0:
					u.make_comment(p,comment,None)
			except:
				pass
			try:
				op = request.POST['operation']
				if op == 'like':
					flag = u.like(p)
				if op == 'dislike':
					flag = u.dislike(p)
			except:
				pass
			try:
				delete_id = request.POST['delete']
				d_post = Post.objects.get(post_id=delete_id)
				print(d_post,type(d_post))
				d_post = Post.objects.get(post_id=delete_id).delete()
				print("delete")
				return HttpResponseRedirect(reverse('insta:profile',args=(uid,)))
			except:
				pass
		clist = p.get_comments()
		context = {
			'user':u,			
			'post':p,
			'pid':post_id,
			'session_id':uid,
			'session_user':UserModel.objects.get(uid=uid),
			'clist':clist,
			'owner':owner
		}
		if flag=='like':
			context['like'] = True
		if flag=='dislike':
			context['dislike'] = True
		return render(request, 'insta/like_dislike.html', context)
	else:
		logout(request)
		return redirect('insta:index')

@login_required
def visit_profile(request,uid,visit_uid):
	print(visit_uid)
	like = dislike = None
	if request.session['uid']==uid:
		if uid == visit_uid:
			return HttpResponseRedirect(reverse('insta:profile',args=(uid,)))	
		message = ''
		su = UserModel.objects.get(uid=uid)
		if su.is_follow(visit_uid) == True:
			message = 'Unfollow'
			dislike = True
		else:
			message = 'Follow'
			like = True
		if request.method=='POST':
			b_user = UserModel.objects.get(uid=visit_uid)
			if request.POST['operation']=='Follow':
				su.follow_user(b_user)
				message = 'Unfollow'
				dislike = True
				like = False
			if request.POST['operation']=='Unfollow':
				su.unfollow_user(b_user)
				message = 'Follow'
				like = True
				dislike = False
		u = UserModel.objects.get(uid=visit_uid)
		u.calculateFollow()
		u.calculateScore()
		a = Post.objects.filter(uid = u).order_by('-post_time')	
		for i in a:
			i.calculateScore()	
		context = {
			'user':u,			
			'allPosts':a,
			'session_id':uid,
			'session_user':UserModel.objects.get(uid=uid),
			'message':message,
		}
		if like == True:
			context['like'] = like
		if dislike == True:
			context['dislike'] = dislike
		return render(request, 'insta/visit_profile.html',context )
	else:
		logout(request)
		return redirect('insta:index')


def report(request):
	allUsers = UserModel.objects.all()[1]
	x = allUsers.get_ordered_post()
	y = allUsers.get_ordered_like()

	return render(request, 'insta/report.html', {
			'allUsers':x,
			'y':y,
		})

@login_required
def upload(request):
	try:
		uid = request.session['uid']
		u = UserModel.objects.get(uid=uid)			
		form = PostForm()
		return render(request, 'insta/upload_post.html', {
			'user':u,
			'form':form,
			'session_id':uid,
			'session_user':UserModel.objects.get(uid=uid),
		})
	except:
		logout(request)
		return redirect('insta:index')

@login_required
def upload_no_view(request):
	print(request.POST,request.FILES)
	uid = request.session['uid']
	u = UserModel.objects.get(uid=uid)
	if request.method == 'POST':		
		form = PostForm(request.POST,request.FILES)		
		if form.is_valid():
			image = form.cleaned_data['image']
			caption = form.cleaned_data['caption']			
			u.make_post(image,caption)			
	else:
		form =  PostForm()
	return HttpResponseRedirect(reverse('insta:profile',args=(u.uid,)))	

@login_required
def follow(request):
	uid = request.session['uid']
	u = UserModel.objects.get(uid=uid)
	message = ''
	search = None
	status = None
	if request.method == 'POST':
		print(request.POST)
		try:
			b_user = UserModel.objects.get(username=request.POST['b_user'])
			if request.POST['operation']=='Follow':
				u.follow_user(b_user)
			if request.POST['operation']=='Unfollow':
				u.unfollow_user(b_user)
		except:
			try:
				search = UserModel.objects.get(username=request.POST['search'])
				if u.is_follow(search.uid):
					status = 'Unfollow'
				else:
					status = 'Follow'
			except:
				message = "The username does not exist"
	ulist = u.get_follow_list()
	ex_list = []
	for i in ulist:
		ex_list.append(i.uid)
	ex_list.append(u.uid)
	full_list = UserModel.objects.exclude(uid__in=ex_list)
	return render(request, 'insta/follow.html', {
		'user':u,
		'ulist':ulist,
		'full_list':full_list,
		'session_id':uid,
		'session_user':UserModel.objects.get(uid=uid),
		'search':search,
		'message':message,
		'status':status,
		})

@login_required
def feed(request):
	uid = request.session['uid']
	u = UserModel.objects.get(uid=uid)
	u.calculateScore()
	plist = u.get_follow_post_list()
	try:
		for i in plist:
			i.calculateScore()
	except:
		pass
	flist = Post.objects.order_by('-post_time')
	for i in flist:
		i.calculateScore()
	return render(request,'insta/feed.html',{
		'session_id':uid,
		'session_user':UserModel.objects.get(uid=uid),
		'allPosts':plist,
		'fullPosts':flist,
		'user':u,
		})

@login_required
def edit(request):
	uid = request.session['uid']
	u = UserModel.objects.get(uid=uid)
	return render(request,'insta/edit.html',{
		'session_id':uid,
		'session_user':UserModel.objects.get(uid=uid),
		'user':u,
		'form':ImageForm(),
		'bform':BioForm(),
		'pform':ProfileForm()
		})

@login_required
def edit_no_view(request):
	uid = request.session['uid']
	u = UserModel.objects.get(uid=uid)
	try:
		if request.POST['edit'] == 'image':
			form = ImageForm(request.POST,request.FILES)
			if form.is_valid():
				u.profile_image = form.cleaned_data['image']
				u.save()
		elif request.POST['edit']== 'bio':
			form = BioForm(request.POST,request.FILES)
			if form.is_valid():
				u.bio = form.cleaned_data['bio']
				u.save()
		elif request.POST['edit']== 'profile_name':
			form = ProfileForm(request.POST,request.FILES)
			if form.is_valid():
				u.profile_name = form.cleaned_data['profile_name']
				u.save()
		return HttpResponseRedirect(reverse('insta:edit'))
	except:
		delete_id = request.POST['delete']
		delete_user = UserModel.objects.get(uid=delete_id)
		logout(request)
		delete_user.delete()
		return HttpResponseRedirect(reverse('insta:login'))

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():			
			password = form.cleaned_data['password']
			username = form.cleaned_data['username']
			rep = request.POST['psw-repeat']
			email = form.cleaned_data['email']
			pname = form.cleaned_data['profile_name']
			
			if rep != password:
				return render(request, 'insta/signup.html', {
					'form':form,
					'error':'The passwords do not match'
				})

			try:
				UserModel.objects.create_user(
				username=username,
				password = password,
				email = email,
				profile_name = pname
				)
				return HttpResponseRedirect(reverse('insta:login'))
			except:
				return render(request, 'insta/signup.html', {
					'form':form,
					'error':'The account already exists'
				})

	else:
		form = SignupForm()
	return render(request, 'insta/signup.html', {'form':form})
"""class UserCreateView(CreateView):
    model = User
    fields = ('User Name', '', 'password', 'email')
    template_name = 'insta/user_form.html'
    success_url = 'insta:signup'

def login(request):
	all_users = UserModel.objects.all()
	context = {
	'all_users':all_users,
	}
	return render(request, 'insta/select.html', context)

def profile(request, user_name):
	user = UserModel.objects.get(username=user_name)
	allPosts = UserModel.post_set.all()
	context = {
	'user':user,
	'allPosts':allPosts,
	}
	return render(request, 'insta/profile.html', context)

def followers(request, user_name):
	user = UserModel.objects.get(username=user_name)
	context = {'user_name':user_name}
	return render(request, 'insta/followers.html', context)

def following(request, user_name):
	user = UserModel.objects.get(username=user_name)
	context = {'user':user}
	return render(request, 'insta/following.html', context)"""