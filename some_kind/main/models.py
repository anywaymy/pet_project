from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to="post_images")
    description = models.TextField(max_length=500)

    def save(self, *args):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args)

    def __str__(self):
        return self.name


class SendMessage(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=60)
    textarea = models.TextField(max_length=500)

    def __str__(self):
        return self.name