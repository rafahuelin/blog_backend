from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField


class Article(models.Model):
    # image = models.ImageField()
    image = ThumbnailerImageField(upload_to='photos', blank=True)
    tags = TaggableManager()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.translation.first().slug


class Translation(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, related_name='translation')
    slug = models.SlugField(max_length=255)
    content = RichTextField()
    language = models.CharField(max_length=30, choices=settings.LANGUAGES)

    def __str__(self) -> str:
        return self.slug