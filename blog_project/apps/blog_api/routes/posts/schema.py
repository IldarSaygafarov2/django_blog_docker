from ninja import Schema
from apps.blog_api.routes.categories.schema import CategorySchema
from datetime import datetime
from apps.blog_api.routes.users.schema import UserSimpleSchema

class PostBaseSchema(Schema):
    id: int
    name: str
    views: int
    category: CategorySchema
    author: UserSimpleSchema
    created_at: datetime
    updated_at: datetime


class PostListSchema(PostBaseSchema):
    short_description: str
    preview: str | None

class PostImageSchema(Schema):
    id: int
    photo: str

class PostCommentSchema(Schema):
    id: int
    text: str
    author: UserSimpleSchema
    created_at: datetime

class PostCommentCreateSchema(Schema):
    text: str

class PostDetailSchema(PostBaseSchema):
    full_description: str | None
    total_likes: int
    total_dislikes: int
    total_comments: int
    images: list[PostImageSchema]
    comments: list[PostCommentSchema]

    @staticmethod
    def resolve_total_likes(instance):
        return instance.likes.user.all().count()

    @staticmethod
    def resolve_total_dislikes(instance):
        return instance.dislikes.user.all().count()

    @staticmethod
    def resolve_total_comments(instance):
        return instance.comments.all().count()

class PostCreationSchema(Schema):
    name: str
    short_description: str
    full_description: str | None = None
    category_id: int


class PostUpdateSchema(Schema):
    name: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    category_id: int | None = None
    author_id: int | None = None

class PostVoteSchema(Schema):
    user: str
    likes: int
    dislikes: int