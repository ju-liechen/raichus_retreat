from django.contrib import admin
from .models import (
    Category,
    Comment,
    Like,
    Post
)

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)
