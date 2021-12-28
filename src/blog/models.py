from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Article(models.Model):
    image = models.ImageField()
    tags = TaggableManager()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.translation_set.first().slug


class Translation(models.Model):
    LANGUAGES = (
        ('en', _('English')),
        ('de', _('German')),
    )

    article = models.ForeignKey(Article, on_delete=DO_NOTHING, null=True)
    slug = models.SlugField(max_length=255)
    content = RichTextField()
    language = models.CharField(max_length=30, choices=LANGUAGES)
