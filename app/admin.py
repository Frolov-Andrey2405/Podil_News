from django.contrib import admin

from .models import Article, Statistics, Tag


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    """
    Customize admin interface for Statistics model.
    """

    def has_add_permission(self, request):
        """
        Prohibit creation of new statistical objects.
        """
        return Statistics.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        """
        Prohibit deletion of statistics.
        """
        return False


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Customize admin interface for Tag model.
    """

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Customize admin interface for Article model.
    """

    list_display = ("title", "author", "created_date", "is_published")
    list_filter = ("is_published", "created_date", "tags")
    search_fields = ("title", "content", "author")
    date_hierarchy = "created_date"
    filter_horizontal = ("tags",)
