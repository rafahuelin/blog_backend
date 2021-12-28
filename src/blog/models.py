from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.conf import settings


class Article(models.Model):
    image = models.ImageField()
    tags = TaggableManager()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.translation.first().slug


class Translation(models.Model):
    article = models.ForeignKey(Article, on_delete=DO_NOTHING, null=True, related_name='translation')
    slug = models.SlugField(max_length=255)
    content = RichTextField()
    language = models.CharField(max_length=30, choices=settings.LANGUAGES)

    def __str__(self) -> str:
        return self.slug