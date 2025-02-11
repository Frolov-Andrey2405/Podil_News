from django.db import models
from django.utils import timezone


class Statistics(models.Model):
    """
    Model for storing general statistics
    """

    grateful_students = models.PositiveIntegerField(
        default=0, verbose_name="Кількість вдячних студентів"
    )
    diplomas = models.PositiveIntegerField(default=0, verbose_name="Кількість грамот")
    articles_count = models.PositiveIntegerField(
        default=0, verbose_name="Кількість статей"
    )

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"

    def __str__(self):
        """
        Return string representation of the object
        """
        return "Загальна статистика"


class Tag(models.Model):
    """
    Model for storing tags
    """

    name = models.CharField(max_length=50, unique=True, verbose_name="Назва тегу")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        """
        Return string representation of the object
        """
        return self.name


class Article(models.Model):
    """
    Model for storing articles
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Зміст")
    author = models.CharField(max_length=100, verbose_name="Автор")
    image = models.ImageField(upload_to="articles/", verbose_name="Зображення")
    created_date = models.DateField(
        default=timezone.now, verbose_name="Дата публікації"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="articles", verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"

    def __str__(self):
        """
        Return string representation of the object
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Update the articles count in statistics model when article is published
        """
        # If this is a new article (not yet saved in the database)
        if not self.pk and self.is_published:
            # Obtain or create a statistics object
            stats, created = Statistics.objects.get_or_create(pk=1)
            stats.articles_count += 1
            stats.save()
        super().save(*args, **kwargs)

    def get_reading_time(self):
        """
        Return the reading time of the article in minutes
        """
        words = len(self.content.split())
        minutes = max(1, words // 150)  # Approximately 150 words per minute
        return minutes
