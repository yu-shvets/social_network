from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "{}".format(self.title)
