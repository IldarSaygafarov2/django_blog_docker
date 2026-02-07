from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import (
    CategoryModel,
    Post,
    Comment,
    PostGalltery,
    PostViewsCount,
    Like,
    Dislike
)
from .forms import CommentForm, PostForm
from django.core.paginator import Paginator
from django.views.generic import UpdateView, DeleteView
from apps.common.utils import update_post_views,add_vote

def add_like_or_dislike(request, pk, action):
    post = get_object_or_404(Post, pk=pk)

    add_vote(request, post, action)

    return redirect('post-detail', pk)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'main/post_confirm_delete.html'
    success_url = '/'

class PostUpdateView(UpdateView):
    model = Post
    #success_url = '/'
    form_class = PostForm
    template_name = 'main/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Изменить'
        return context


def show_home_page(request):
    #orm
    # categories = CategoryModel.objects.all()
    posts = Post.objects.all()

    for post in posts:
        try:
            post.likes
        except Exception as e:
            Like.objects.create(post=post)

        try:
            post.dislikes
        except Exception as e:
            Dislike.objects.create(post=post)

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    context = {
     #   'categories': categories,
        'posts': posts
    }

    return render(request, 'main/index.html', context)


def contacts_view(request):
    return render(request, 'main/contacts.html')

def show_post_by_category(request, pk):
    category = CategoryModel.objects.get(pk=pk)
    posts = Post.objects.filter(category = category)
    context = {
        'posts': posts,
        'category': category
    }
    return render(request,'main/category_posts.html', context)

def show_post_detail_page(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.author = request.user
            form.save()
            return redirect('post-detail', post.id)
    else:
        form = CommentForm()

    update_post_views(request, post)

    context = {
        'post': post,
        'form': form
    }
    return render(request, 'main/post_detail.html', context)

def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('post-detail', comment.post.id)

def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files = request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()

            photos = request.FILES.getlist('photos')
            for photo in photos:
                PostGalltery.objects.create(
                    post=form,
                    photo=photo
                )


            return redirect('post-detail', form.id)
    else:
        form = PostForm()

    context = {
        'title': 'Создать',
        'form': form
    }
    return render(request, 'main/post_form.html', context)

def search_posts(request):
    search_query = request.GET.get('q')

    if search_query:
        posts = Post.objects.filter(name__iregex=search_query)
    else:
        posts = Post.objects.all()

    context={
        'found_posts': posts,
        'seqrch_query': search_query
    }
    return render(request, 'main/search_results.html', context)