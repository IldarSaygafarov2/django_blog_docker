from ninja import Router
from.schema import CategorySchema, CategoryCreationSchema, CategoryUpdateSchema
from apps.main.models import CategoryModel
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth

categories_router = Router(
    tags=['Categories']
)

@categories_router.get('/categories/', response=list[CategorySchema])
def get_categories(request):
    return CategoryModel.objects.all

@categories_router.post('/categories/', response=CategorySchema, auth=JWTAuth())
def create_category(request, data: CategoryCreationSchema):
    category = CategoryModel.objects.create(name=data.name)
    return category

@categories_router.get("/categories/{pk}/", response = CategorySchema)
def get_category_by_id(request, pk: int):
    category = get_object_or_404(CategoryModel, pk=pk)
    return category

@categories_router.delete("/categories/{pk}/")
def delete_category_by_id(request, pk: int):
    category = get_object_or_404(CategoryModel, pk=pk)
    category.delete()
    return True

@categories_router.put("/categories/{pk}", response=CategorySchema)
def update_category(request, pk: int, data: CategoryUpdateSchema):
    category = get_object_or_404(CategoryModel, pk=pk)
    category.name = data.name
    category.save()
    return category