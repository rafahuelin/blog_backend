from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    fields = ('slug', 'image', 'tags', 'content', 'creation_date', )
    list_display = ('slug', 'tag_list', 'creation_date', )
    list_filter = ('tags', )
    readonly_fields = ('creation_date', )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Article, ArticleAdmin)
