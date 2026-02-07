from ninja import Router

from .categories.handlers import categories_router
from .posts.handlers import posts_router
from .users.handlers import users_router

api_router = Router()

api_router.add_router('/v1/', categories_router)
api_router.add_router('/v1/', posts_router)
api_router.add_router('/v1/', users_router)