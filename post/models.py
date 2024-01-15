from django.db import models

from category.models import Category

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.SET_NULL, null=True)
    preview = models.ImageField(upload_to='images', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    SearchableFields = ['title', 'body']




    def __str__(self):
        return f'{self.owner} - {self.title[:25]}'

    class Meta:
        ordering = ('created_at',)


class PostImage(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)



