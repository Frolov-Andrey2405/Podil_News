from django import template

register = template.Library()

@register.filter
def reading_time(word_count):
    """
    Calculate the estimated reading time in minutes based on word count.
    """

    words_per_minute = 150  # Average reading speed
    return max(1, round(word_count / words_per_minute))  # At least 1 minute
