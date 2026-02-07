from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from apps.main.models import Post, Like, Dislike

# Create your views here.

def show_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def show_registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }

    return render(request, 'users/registration.html',context)

def logout_user(request):
    logout(request)
    return redirect ('home')

def _get_user_posts_data(posts):
    total_comments = [post.comments.all().count() for post in posts]
    total_views = [post.views for post in posts]
    total_likes = [post.likes.user.all().count() for post in posts]
    total_dislikes = [post.dislikes.user.all().count() for post in posts]
    return total_dislikes,total_likes,total_views,total_comments

def show_profile_page(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    total_comments, total_likes, total_dislikes, total_views = _get_user_posts_data(posts)

    context = {
        'user': user,
        'posts': posts,
        'total_comments' : sum(total_comments),
        'total_views' : sum(total_views),
        'total_likes': sum(total_likes),
        'total_dislikes': sum(total_dislikes)
    }
    return render (request, "users/profile.html", context)

def show_author_profile_page(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    total_comments, total_likes, total_dislikes, total_views = _get_user_posts_data(posts)

    context = {
        'user': user,
        'posts': posts,
        'total_comments' : sum(total_comments),
        'total_views' : sum(total_views),
        'total_likes': sum(total_likes),
        'total_dislikes': sum(total_dislikes)
    }
    return render (request, "users/profile.html", context)