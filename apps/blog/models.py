from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, default='')
    body = models.CharField(max_length=10000, default='',
                            blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['created_by', 'post'],
                name='one_user_like_per_post'
            ),
        ]
