from django.shortcuts import render, get_object_or_404
from app.models import Statistics, Article

def index(request):
    """
    Homepage view function.

    This view function renders the index.html template in the main app,
    passing in the statistics object and a list of all published articles.
    """

    # Obtain or create a statistics object
    statistics, created = Statistics.objects.get_or_create(pk=1)
    
    # Getting published articles
    articles = Article.objects.filter(is_published=True)
    
    context = {
        'statistics': statistics,
        'articles': articles,
    }
    return render(request, 'main/index.html', context)

def article_detail(request, article_id):
    """
    Article detail view function.

    This view function renders the article_detail.html template in the main app,
    passing in the article object and the word count of the article content.
    """
    article = get_object_or_404(Article, id=article_id, is_published=True)
    word_count = len(article.content.split())
    return render(request, 'main/article_detail.html', {'article': article, 'word_count': word_count})