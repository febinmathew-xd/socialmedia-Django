from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowerCount, Comment
from itertools import chain
import random




# Create your views here.


@login_required(login_url='login')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile_req = Profile.objects.get(user=user_object)
    posts =Post.objects.all()
    comments = Comment.objects.all()
    

    user_following_list = []
    feed = []
    own_feed = []

    user_following = FollowerCount.objects.filter(followers=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
         host = User.objects.get(username=usernames)
         feed_list = Post.objects.filter(host=host)
         feed.append(feed_list)

    own_feed_list = Post.objects.filter(host=request.user)
    
    for own_list in own_feed_list:
        own_feed.append(own_list)

    feed_list = list(chain(*feed, own_feed))
    
    #user suggestion

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    

    print(user_following_all)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    print(new_suggestions_list)
    current_user = User.objects.filter(id=request.user.id)
    final_suggestions_list = [x for x in list(new_suggestions_list) if(x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    suggestion_profile_list = []

    for user in final_suggestions_list:
        user_profile = Profile.objects.get(user=user)
        suggestion_profile_list.append(user_profile)

    
    
    print(suggestion_profile_list)
    context = {"user_profile":user_profile_req, 'posts':feed_list, 'comments':comments, 'suggestion_profile_list':suggestion_profile_list}
    return render(request, 'index.html', context)


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # loguser in and redirect to settings page
                 
                user_login = authenticate(username=username, password=password)
                login(request, user_login)


                # create a profile object for the new user

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password doesnt match')
            return redirect('signup')

    else:
       return render(request, 'signup.html')



def loginUser(request):

    if request.user.is_authenticated :
        return redirect('home')
    
    if request.method == 'POST':
        
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.info(request, "user doesnt exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            messages.info(request, 'username or password doesnt exist')
            return redirect('login')

    else:
      return render(request, 'signin.html')
    

@login_required(login_url='login')
def logoutUser(request):
     logout(request)
     return redirect('login')
    
@login_required(login_url='login')
def settings(request):

    user_profile = Profile.objects.get(user=request.user)

    context = {'user_profile':user_profile}

    if request.method == 'POST':
       
       if request.FILES.get('image') == None:
           image = user_profile.avatar
           bio = request.POST.get('bio')
           location = request.POST.get('location')

           user_profile.avatar = image
           user_profile.bio = bio
           user_profile.location = location
           user_profile.save()
           
       if request.FILES.get('image') != None:
           image = request.FILES.get('image')
           bio = request.POST.get('bio')
           location = request.POST.get('location')

           user_profile.avatar = image
           user_profile.bio = bio
           user_profile.location = location
           user_profile.save()

       return redirect('home')
        
    return render(request, 'setting.html', context)


@login_required(login_url='login')
def upload(request):

    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        profile = Profile.objects.get(user=user)

        new_post = Post.objects.create(host=user, image=image, caption=caption, host_profile=profile)
        new_post.save()
        return redirect('home')
    else:
        return redirect('home')

    
@login_required(login_url='login')
def profile(request, pk):
        user = User.objects.get(id=pk)
        user_profile = Profile.objects.get(user = user)
        user_posts = Post.objects.filter(host=user)
        post_count = user_posts.count()
        follower = request.user.username
        user = user.username
        followers_count = FollowerCount.objects.filter(user=user).count()
        following_count = FollowerCount.objects.filter(followers=user).count()

        if FollowerCount.objects.filter(followers=follower, user=user).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'


        context = {
                     "user":user, 
                     'user_profile':user_profile, 
                     'user_posts':user_posts,
                     'post_count':post_count,
                     'button_text':button_text,
                     'followers_count':followers_count,
                     'following_count':following_count
                     }
        

        return render(request, 'profile.html', context)    



@login_required(login_url='login')
def like_post(request,pk):

    username = request.user.username
    

    post = Post.objects.get(id=pk)
    post_id = post.id

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('home')
    else:
        like_filter.delete()
        post.no_of_likes-=1
        post.save()
        return redirect('home')


    

@login_required(login_url='login')
def deletePost(request,pk):
    
    post = Post.objects.get(id=pk)
    if request.user == post.host:
        post.delete()
        return redirect('home')

    else:
        return HttpResponse('You are not permitted to delete')

@login_required(login_url='home')
def follow(request):
        
    if request.method == 'POST':
        user = request.POST.get('user')
        follower = request.POST.get('follower')
        user_profile = User.objects.get(username=user)
        user_id = user_profile.id

        print(user)
        print(follower)
        print(user_id)
         

        if FollowerCount.objects.filter(followers=follower, user=user).first():
            delete_follower = FollowerCount.objects.get(followers=follower, user=user)
            delete_follower.delete()
            return redirect(f'profile/{user_id}')
        
        else:
            new_follower = FollowerCount.objects.create(followers=follower, user=user)
            new_follower.save()
            return redirect(f'profile/{user_id}')



@login_required(login_url='login')
def commentPost(request):
    

    if request.method == 'POST':
        user = request.user
        user_profile = Profile.objects.get(user=user)
        post_comment = request.POST.get('comment')
        post_id =  request.POST.get('postid')
        post = Post.objects.get(id=post_id)

        if post_comment == None:
            return redirect('home')
        
        else:
            new_comment = Comment.objects.create(comment_profile=user_profile, post_comment=post_comment, comment_post=post)
            new_comment.save()
            return redirect('home')
        
    else:
        return redirect('home')


@login_required(login_url='login')
def search(request):
     
     req_user = request.user
     req_user_profile = Profile.objects.get(user=req_user)

     if request.method == 'POST':
         username = request.POST.get('username')
         username_user = User.objects.filter(username__icontains=username)

    
     profile_list = []

     for user in username_user:
         user_profile = Profile.objects.get(user=user)

         profile_list.append(user_profile)
        
     print(profile_list)

  
     context = {
         'req_user_profile':req_user_profile, 
          'username_user':username_user,
          "username":username,
          'profile_list':profile_list,
         }

     return render(request, 'search.html', context)





    
        