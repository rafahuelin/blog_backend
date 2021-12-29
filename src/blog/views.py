from django.http.response import Http404
from django.shortcuts import render, get_object_or_404
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
            'image': f'media/{article.image}'
        })
    return articles_list


def article_list(request):
    filtered_articles = Article.objects.filter(translation__language=request.LANGUAGE_CODE)
    articles = create_article_list(filtered_articles, request.LANGUAGE_CODE)
    context = {
        'articles': articles,
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
