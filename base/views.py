from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Post

# Create your views here.


@login_required(login_url='login')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts =Post.objects.all()
    context = {"user_profile":user_profile, 'posts':posts}
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
            messages.error(request, "user doesnt exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request, 'username or password doesnt exist')
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

        new_post = Post.objects.create(host=user, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    else:
        return redirect('home')

    

def profile(request, pk):
        user = User.objects.get(id=pk)
        user_profile = Profile.objects.get(user = user)
        context = {"user":user, 'user_profile':user_profile}
        

        return render(request, 'profile.html', context)    