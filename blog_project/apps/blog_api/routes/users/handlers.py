from ninja import Router
from .schema import UserSchema, UserRegisterSchema
from django.contrib.auth.models import User
from ninja.errors import ValidationError
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth

users_router = Router(
    tags=['Users']
)

@users_router.get('/users/', response=list[UserSchema])
def get_users(request):
    users = User.objects.all()
    return users

@users_router.post('/users/login/')
def login_user(request, login_data):
    pass

@users_router.post('/users/register/', response=UserSchema)
def register_user(request, register_data: UserRegisterSchema):
    is_username_exists = User.objects.filter(username=register_data.username).exists()
    if is_username_exists:
        raise ValidationError(f'user with username={register_data.username} already exists')

    is_email_exists = User.objects.filter(email=register_data.email).exists()
    if is_email_exists:
        raise ValidationError(f'user with email={register_data.email} already exists')

    if len(register_data.password1) < 8:
        raise ValidationError('password must contain more than 8 chars')

    if register_data.password1 != register_data.password2:
        raise ValidationError('passwords are not same')

    new_user = User.objects.create(
        username=register_data.username,
        email=register_data.email,
        first_name=register_data.first_name,
        password=register_data.password1
    )
    return new_user

@users_router.get('/users/logout/')
def logout_user(request):
    pass

@users_router.get('/users/me/', auth=JWTAuth(), response=UserSchema)
def get_user_me(request):
    return request.auth

@users_router.get('/users/{username}/', response=UserSchema)
def get_user(request, username):
    user = get_object_or_404(User, username=username)
    return user