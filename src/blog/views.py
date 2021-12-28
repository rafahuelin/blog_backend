from django.shortcuts import render
from blog.models import Article
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
