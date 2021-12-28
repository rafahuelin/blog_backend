from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Article(models.Model):
    slug = models.SlugField(max_length=255)
    image = models.ImageField()
    tags = TaggableManager()
    content = RichTextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.slug
