from django.shortcuts import render
from blog.models import Article, Translation


def create_article_list(articles, language):
    articles_list = []
    for article in articles:
        articles_list.append({
            'id': article.id,
            'slug': article.translation.get(language=language).slug,
            'content': article.translation.get(language=language).content,
            'image': f'media/{article.image}'
        })
    return articles_list


def article_list(request):
    filtered_english_articles = Article.objects.filter(translation__language='en')
    english_articles = create_article_list(filtered_english_articles, 'en')
    german_articles = create_article_list(filtered_english_articles, 'de')
    context = {
        'english_articles': english_articles,
        'german_articles': german_articles,
    }
    return render(request, 'blog/article_list.html', context)

