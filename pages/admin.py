from django.contrib import admin
from .models import Team
from django.utils.html import format_html

"""Admin configuration for the Team model used on public-facing pages."""


class TeamAdmin(admin.ModelAdmin):
    """Display a small photo thumbnail and basic team metadata in the admin list view."""

    def thumbnail(self, object):
        """Return an HTML image element for the team member's profile photo."""
        return format_html('<img src="{}" width="40" />'.format(object.photo.url))

    thumbnail.short_description = 'Photo'

    list_display = ('id', 'thumbnail', 'first_name', 'last_name', 'designation', 'created_date')
    list_display_links = ('id', 'thumbnail', 'first_name',)
    search_fields = ('first_name', 'last_name', 'designation')
    list_filter = ('designation',)


admin.site.register(Team, TeamAdmin)
