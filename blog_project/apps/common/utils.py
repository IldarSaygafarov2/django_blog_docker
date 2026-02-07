from apps.main.models import PostViewsCount

def update_post_views(request, post):
    if request.user.is_authenticated:
        viewed_post, post_created = PostViewsCount.objects.get_or_create(
        post=post,
        author=request.user
        )
        if post_created:
            post.views += 1
            post.save()


def add_vote(request, post, _type):
    user = request.auth
    if _type == 'add_like':
        if user in post.likes.user.all():
            post.likes.user.remove(user.id)
        else:
            post.likes.user.add(user.id)
            post.dislikes.user.remove(user.id)
    elif _type == 'add_dislike':
        if user in post.dislikes.user.all():
            post.dislikes.user.remove(user.id)
        else:
            post.dislikes.user.add(user.id)
            post.likes.user.remove(user.id)
