from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from app.templatetags.custom_filters import reading_time

from .models import Article, Statistics, Tag


@admin.register(Statistics)
class StatisticsAdmin(ModelAdmin):
    """
    Enhanced admin interface for Statistics model with visual improvements.
    """

    list_display = ("id", "display_students", "display_diplomas", "display_articles")
    readonly_fields = ("grateful_students", "diplomas", "articles_count")

    def display_students(self, obj):
        """
        Display grateful students count in a visually appealing way.
        """
        return format_html(
            '<div style="text-align: center;">'
            '<div style="font-size: 24px; color: #4CAF50;">{}</div>'
            '<div style="color: #666;">Вдячних студентів</div>'
            "</div>",
            obj.grateful_students,
        )

    display_students.short_description = "Студенти"

    def display_diplomas(self, obj):
        """
        Display diplomas count in a visually appealing way.
        """
        return format_html(
            '<div style="text-align: center;">'
            '<div style="font-size: 24px; color: #2196F3;">{}</div>'
            '<div style="color: #666;">Грамот</div>'
            "</div>",
            obj.diplomas,
        )

    display_diplomas.short_description = "Грамоти"

    def display_articles(self, obj):
        """
        Display articles count in a visually appealing way.
        """
        return format_html(
            '<div style="text-align: center;">'
            '<div style="font-size: 24px; color: #FF5722;">{}</div>'
            '<div style="color: #666;">Статей</div>'
            "</div>",
            obj.articles_count,
        )

    display_articles.short_description = "Статті"

    def has_add_permission(self, request):
        """
        Prevent adding new statistics objects if one already exists.
        """
        return Statistics.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting the statistics object.
        """
        return False


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """
    Enhanced admin interface for Tag model with usage statistics.
    """

    list_display = ("name", "articles_count", "display_usage_badge")
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        """
        Return a queryset of Tag objects annotated with the count of related articles.

        This method overrides the default queryset to include an additional annotation
        that counts the number of articles associated with each Tag object.
        """

        queryset = super().get_queryset(request)
        return queryset.annotate(articles_count=Count("articles"))

    def articles_count(self, obj):
        """
        Return the number of articles associated with the tag.
        """
        return obj.articles_count

    articles_count.admin_order_field = "articles_count"
    articles_count.short_description = "Кількість статей"

    def display_usage_badge(self, obj):
        """
        Return a colored badge indicating the usage of the tag.

        The badge is colored based on the number of articles associated with the tag.
        If the number of articles is greater than 10, the badge is green and labeled as "Популярний".
        If the number of articles is greater than 5, the badge is blue and labeled as "Активний".
        If the number of articles is greater than 0, the badge is yellow and labeled as "Використовується".
        Otherwise, the badge is gray and labeled as "Не використовується".
        """
        if obj.articles_count > 10:
            color = "#4CAF50"
            text = "Популярний"
        elif obj.articles_count > 5:
            color = "#2196F3"
            text = "Активний"
        elif obj.articles_count > 0:
            color = "#FFC107"
            text = "Використовується"
        else:
            color = "#9E9E9E"
            text = "Не використовується"

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 0.8em;">{}</span>',
            color,
            text,
        )

    display_usage_badge.short_description = "Статус"


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    """
    Enhanced admin interface for Article model with advanced features.
    """

    list_display = (
        "title",
        "display_author",
        "created_date",
        "display_status",
        "display_reading_time",
        "display_tags",
        "article_preview_button",
    )
    list_filter = ("is_published", "created_date", "tags")
    search_fields = ("title", "content", "author")
    date_hierarchy = "created_date"
    filter_horizontal = ("tags",)
    readonly_fields = ("display_reading_time",)

    fieldsets = (
        ("Основна інформація", {"fields": ("title", "author", "content")}),
        (
            "Медіа",
            {
                "fields": ("image",),
            },
        ),
        (
            "Метадані",
            {
                "fields": (
                    "tags",
                    "created_date",
                    "is_published",
                    "display_reading_time",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def display_author(self, obj):
        """
        Display the author's name in a simple HTML span element.

        This method returns the author's name wrapped in a span element for
        consistent HTML formatting within the admin interface.

        :param obj: The Article object containing the author information.
        :return: An HTML formatted string representing the author's name.
        """

        return format_html("<span>{}</span>", obj.author)

    display_author.short_description = "Автор"

    def display_status(self, obj):
        """
        Return a colored badge indicating the publication status of the article.

        The badge is colored based on the publication status of the article.
        If the article is published, the badge is green and labeled as "Опубліковано".
        If the article is a draft, the badge is yellow and labeled as "Чернетка".
        """

        if obj.is_published:
            color = "#4CAF50"
            text = "Опубліковано"
        else:
            color = "#FFC107"
            text = "Чернетка"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px;">{}</span>',
            color,
            text,
        )

    display_status.short_description = "Статус"

    def display_reading_time(self, obj):
        """
        Return a colored badge indicating the estimated reading time of the article.

        The badge is colored gray and labeled with the estimated reading time in minutes.
        """
        word_count = len(obj.content.split())
        minutes = reading_time(word_count)
        return format_html(
            '<span style="color: #666;">'
            '<i class="fas fa-clock" style="margin-right: 5px;"></i>'
            "{} хв. читання</span>",
            minutes,
        )

    display_reading_time.short_description = "Час читання"

    def display_tags(self, obj):
        """
        Return a string of tags associated with the article, each tag
        wrapped in a gray badge.

        If there are no tags, return a hyphen.
        """
        tags = obj.tags.all()
        if not tags:
            return "-"
        return format_html(
            " ".join(
                f'<span style="background-color: #E0E0E0; color: #333; padding: 2px 6px; '
                f'border-radius: 10px; margin: 0 2px; font-size: 0.8em;">#{tag.name}</span>'
                for tag in tags
            )
        )

    display_tags.short_description = "Теги"

    def article_preview_button(self, obj):
        """
        Return a button that links to the article's detail page.

        The button is labeled "Переглянути" and is styled with a blue background color and white text.
        """
        url = reverse("article_detail", args=[obj.id])
        return format_html(
            '<a href="{}" class="button" style="border-radius: 12px; background-color: #2196F3; padding: 4px 8px;" target="_blank">Переглянути</a>',
            url,
        )

    article_preview_button.short_description = "Перегляд"

    class Media:
        """
        Additional CSS styles for the Django admin interface.

        The 'all' key is a tuple of URLs to load CSS stylesheets for all media types.
        """

        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
            )
        }
