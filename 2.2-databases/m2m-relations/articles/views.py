from django.db.models import Prefetch
from django.shortcuts import render

from articles.models import Article, ArticleScope


def articles_list(request):
    template = 'articles/news.html'
    articles = Article.objects.all().order_by('-published_at'). \
        prefetch_related(
        Prefetch('scopes',
                 queryset=ArticleScope.objects.order_by('-is_main', 'tag__name').all()
                 )
        )
    context = {
        'object_list': articles,
    }

    return render(request, template, context)
