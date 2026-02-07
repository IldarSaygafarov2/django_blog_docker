from ninja import NinjaAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

from apps.blog_api.routes import api_router


api = NinjaExtraAPI(
    title='PROWEB blog api',
    description='This API made for blog'
)
api.register_controllers(NinjaJWTDefaultController)

api.add_router('', api_router)