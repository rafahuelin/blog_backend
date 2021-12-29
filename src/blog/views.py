from django.http.response import Http404
from django.shortcuts import render
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
    tags = [t.slug for t in Tag.objects.all()]
    selected_tags = []
    is_get_request = False
    if request.method == 'POST':
        for tag in tags:
            tag_value = request.POST.get(tag)
            if tag_value == 'on':
                selected_tags.append(tag)
    elif request.method == 'GET':
        selected_tags = tags
        is_get_request = True
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
        language = Translation.objects.get(slug=slug).language
        context = {
            'content': article.translation.get(language=language).content,
            'creation_date': article.creation_date,
            'image': f'/media/{article.image}',
            'slug': slug,
            'title': slug.replace('-', ' ').title(),
        }
    except Article.DoesNotExist:
        raise Http404
    return render(request, "blog/article_detail.html", {'article': context})
