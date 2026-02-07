from ninja import Router, File, UploadedFile
from ninja.errors import ValidationError
from .schema import (PostListSchema,
                     PostDetailSchema,
                     PostCreationSchema,
                     PostUpdateSchema,
                     PostVoteSchema,
                     PostCommentCreateSchema,
                     PostCommentSchema)
from apps.main.models import Post, CategoryModel, Like, Dislike, PostGalltery, Comment
from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User # если юзер не менялся
from django.contrib.auth import get_user_model
import os
from apps.common.utils import update_post_views, add_vote
from ninja_jwt.authentication import JWTAuth


User = get_user_model()


posts_router = Router(
    tags=['Posts']
)

@posts_router.get('/posts/', response=list[PostListSchema])
def get_posts(request):
    posts = Post.objects.all()
    return posts

@posts_router.post('/posts/', response=PostDetailSchema, auth=JWTAuth())
def create_post(request,
                post_data: PostCreationSchema,
                preview: File[UploadedFile | None]  = None,
                photos: File[list[UploadedFile ] | None]  = None
):
    author = request.auth # авторизованный пользователь
    category = get_object_or_404(CategoryModel, pk=post_data.category_id)

    new_post = Post.objects.create(
        name=post_data.name,
        short_description=post_data.short_description,
        full_description=post_data.full_description,
        author=author,
        category=category
    )
    try:
        new_post.likes
    except Exception as e:
        Like.objects.create(post=new_post)

    try:
        new_post.dislikes
    except Exception as e:
        Dislike.objects.create(post=new_post)

    if preview is not None:
        new_post.preview = preview
        new_post.save()

    if photos is not None:
        for photo in photos:
            PostGalltery.objects.create(
                post=new_post,
                photo=photo
            )
    return new_post

@posts_router.get("/post/{pk}", response=PostDetailSchema)
def get_post_by_id(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    update_post_views(request, post)
    return post

@posts_router.delete("/post/{pk}", auth=JWTAuth())
def get_delete_by_id(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.auth:
        raise ValidationError('Permission denied')
    post.delete()
    return True

@posts_router.patch("/post/{pk}", response=PostDetailSchema, auth=JWTAuth())
def update_post(request,
                pk: int,
                data: PostUpdateSchema,
                preview: File[UploadedFile | None]= None,
                photos: File[list[UploadedFile] | None] = None
                ):

    # author = get_object_or_404(User, pk=data.author_id)
    # category = get_object_or_404(CategoryModel, pk=data.category_id)

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.auth:
        raise ValidationError('Permission denied')

    post_data = data.model_dump()

    for key, value in post_data.items():
        if value is not None:
            setattr(post, key, value)
    from django.conf import settings
    preview_folder_path = settings.BASE_DIR / 'media' / 'articles' / 'previews'

    previews_folder_images = os.listdir( preview_folder_path )
    current_preview_filename = post.preview.url.split('/')[-1] if post.preview else None
    if current_preview_filename is not None and current_preview_filename in previews_folder_images:
       path = preview_folder_path / current_preview_filename
    os.remove(path)

    if preview is not None:
        post.preview = preview

    # post_gallery_folder_path = settings.BASE_DIR / 'media' / 'articles' / 'galleries' / f'post-{post.id}'
    # post_gallery_images = os.listdir(post_gallery_folder_path)
    # if photos is not None:
    #     for image_obj in post.images.all():
    #         filename = image_obj.photo.url.split('/')[-1]

    post.save()
    return post

@posts_router.post('/posts/{pk}/like/', response=PostVoteSchema, auth=JWTAuth())
def add_like(request, pk):

    post = get_object_or_404(Post, pk=pk)

    add_vote(request, post, 'add_like')

    return {
        'user': request.user.username,
        'likes': post.likes.user.count(),
        'dislikes': post.dislikes.user.count()
    }

@posts_router.post('/posts/{pk}/dislike/', response=PostVoteSchema, auth=JWTAuth())
def add_dislike(request, pk):

    post = get_object_or_404(Post, pk=pk)

    add_vote(request, post, 'add_dislike')

    return {
        'user': request.user.username,
        'likes': post.likes.user.count(),
        'dislikes': post.dislikes.user.count()
    }

@posts_router.post('/posts/{pk}/comments/create/', response=PostCommentSchema,auth=JWTAuth())
def create_comment(request, pk, comment_data: PostCommentCreateSchema):

    post = get_object_or_404(Post, pk=pk)

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        text=comment_data.text
    )
    return comment

@posts_router.delete('/posts/{pk}/comments/{comment_pk}/delete', auth=JWTAuth())
def delete_comment(request, pk,comment_pk):
    user = request.auth
    if not user.is_superuser:
        raise ValidationError('Permission denied')
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if comments:
        comment = comments.filter(pk=comment_pk).first()
        if comment is None:
            raise ValidationError('Comment not found')
        comment.delete()
    return True
