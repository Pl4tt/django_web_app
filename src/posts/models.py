from django.db import models
from django.conf import settings


class Post(models.Model):
    content = models.CharField(max_length=500, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name="posts", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date_created", auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content}"


class Comment(models.Model):
    content = models.CharField(max_length=255, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, blank=False, null=False, related_name="comments", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date_created", auto_now_add=True)

    def __str__(self):
        return f"{self.author} in {self.post}: {self.content}"
    

class Like(models.Model):
    post = models.ForeignKey(Post, blank=False, null=False, related_name="likes", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name="likes", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="date_created", auto_now_add=True)

    def __str__(self):
        return f"{self.author} in {self.post}"
    
