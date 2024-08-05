from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleScope, Tag


class ArticleScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        cnt_main = 0
        for form in self.forms:
            is_main = form.cleaned_data.get('is_main', False)
            if is_main:
                cnt_main += 1
            if cnt_main > 1:
                raise ValidationError('Основным разделом может быть только один раздел')
        if cnt_main == 0:
            raise ValidationError('Укажите основной раздел')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleScopeInline(admin.TabularInline):
    model = ArticleScope
    extra = 2
    formset = ArticleScopeInlineFormset
    verbose_name = 'Тематика статьи'
    verbose_name_plural = 'Тематики статьи'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleScopeInline, ]
    list_filter = ['scopes', ]


@admin.register(Tag)
class ScopeAdmin(admin.ModelAdmin):
    pass
