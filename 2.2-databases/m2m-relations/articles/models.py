from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        through='ArticleScope',
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class ArticleScope(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='scopes',
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Раздел',
        on_delete=models.CASCADE,
        related_name='scopes',
    )
    is_main = models.BooleanField(verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематики статьи'
        verbose_name_plural = 'Тематики статьи'

    def __str__(self):
        return f'{self.article}: {self.tag}'

