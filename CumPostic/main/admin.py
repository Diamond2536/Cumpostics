from django.contrib import admin
from .models import Post, Comments, PostScreenshot, PostFile, PostType, PostCategory
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CommentsInline(admin.TabularInline):
    model = Comments

class PostFileInline(admin.TabularInline):
    model = PostFile

class PostScreeshotInline(admin.TabularInline):
    model = PostScreenshot

class PostCategoryInline(admin.TabularInline):
    model = PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    inlines = [PostScreeshotInline, PostFileInline, CommentsInline]
    exclude = ['screen', 'file']

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(PostType)
admin.site.register(PostCategory)