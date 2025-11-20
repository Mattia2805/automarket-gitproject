from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html

from .models import Car


class CarAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />' .format(object.car_photo.url))

    thumbnail.short_description = 'Car Image'
    list_display = ('id', 'thumbnail', 'car_title', 'city', 'color', 'model', 'year', 'body_style', 'fuel_type', 'is_featured')
    list_display_links = ('id', 'thumbnail', 'car_title')
    list_editable = ('is_featured',)
    # keep city in search_fields so the base implementation still searches by the stored value
    search_fields = ('id', 'car_title', 'city', 'model', 'body_style', 'fuel_type')
    list_filter = ('city', 'model', 'body_style', 'fuel_type')

    def get_search_results(self, request, queryset, search_term):
        """Also allow searching by the *display* value of the city choice (e.g. 'Tirane')."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            city_q = Q()
            term = search_term.lower()
            for value, label in Car.city_choice:
                if term in str(label).lower():
                    city_q |= Q(city=value)

            if city_q:
                queryset = queryset | self.model.objects.filter(city_q)

        return queryset, use_distinct


admin.site.register(Car, CarAdmin)
