from django.contrib import admin

from post.models import Post

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = Post.SearchableFields