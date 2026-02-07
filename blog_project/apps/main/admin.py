from django.contrib import admin

from .models import CategoryModel, Post, PostGalltery, Comment

class PostGalleryInline(admin.TabularInline):
    model = PostGalltery
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'views', 'created_at', 'category', 'author']
    list_display_links = ['id', 'name']
    list_editable = ['category', 'author']
    list_filter = ['created_at', 'category', 'author']
    readonly_fields = ['views']
    search_fields = ['name']
    inlines = [PostGalleryInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'created_at']
    list_filter = ['post', 'author', 'created_at']

admin.site.register(CategoryModel)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)