from django.http.response import Http404
from django.shortcuts import redirect, render
from taggit.models import Tag
from blog.models import Article, Translation
import logging
logger = logging.getLogger(__name__)


def create_article_list(articles, language):
    articles_list = []
    for article in articles:
        slug = article.translation.get(language=language).slug
        articles_list.append({
            'id': article.id,
            'slug': slug,
            'title': slug.replace('-', ' ').title(),
            'content': article.translation.get(language=language).content,
            'image': f'{article.image["thumbnail"].url}'
        })
    return articles_list


def article_list(request):
    all_tags = Tag.objects.all()
    tags = [{ 'name': t.slug, 'selected': True } for t in all_tags ]
    selected_tags = []
    is_get_request = False
    if request.method == 'POST':
        for tag in tags:
            tag_value = request.POST.get(tag['name'])
            selected = tag_value == 'on'
            tag['selected'] = selected
            if selected: selected_tags.append(tag['name'])
    elif request.method == 'GET':
        selected_tags = [t.slug for t in all_tags]
    articles_by_language = Article.objects.filter(translation__language=request.LANGUAGE_CODE)
    articles_by_language_and_tag = articles_by_language.filter(tags__slug__in=selected_tags).distinct()
    articles = create_article_list(articles_by_language_and_tag, request.LANGUAGE_CODE)

    context = {
        'articles': articles,
        'selected_tags': selected_tags,
        'tags': tags,
        'is_get_request': is_get_request,
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    try:
        article = Article.objects.get(translation__slug=slug)
        lang_slug = article.translation.get(language=request.LANGUAGE_CODE).slug
        if slug != lang_slug:
            return redirect(f'/{lang_slug}')
        language = Translation.objects.get(slug=lang_slug).language
        context = {
            'content': article.translation.get(language=language).content,
            'creation_date': article.creation_date,
            'image': f'{article.image.url}',
            'slug': slug,
            'title': slug.replace('-', ' ').title(),
        }
    except Article.DoesNotExist:
        raise Http404
    return render(request, "blog/article_detail.html", {'article': context})
