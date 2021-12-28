from django.contrib import admin
from .models import Article, Translation
from logging import getLogger

logger = getLogger(__name__)


class TranslationInline(admin.StackedInline):
    model = Translation
    fields = ('slug', 'language', 'content', )
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    fields = ('image', 'tags', 'creation_date', )
    list_display = ('get_slug', 'tag_list', 'creation_date', )
    readonly_fields = ('creation_date', )
    inlines = (TranslationInline, )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
    def get_slug(self, obj):
        return obj.translation_set.first().slug
    
    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]


admin.site.register(Article, ArticleAdmin)
