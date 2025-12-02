from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Car

class CarAdmin(admin.ModelAdmin):

    # Show thumbnail
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" />', object.car_photo.url)
    thumbnail.short_description = 'Car Image'

    # NEW: Generate PDF button
    def generate_report(self, obj):
        url = reverse("car_report_pdf", args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">PDF Report</a>', url)
    generate_report.short_description = "Report"

    list_display = (
        'id',
        'thumbnail',
        'car_title',
        'city',
        'color',
        'model',
        'year',
        'body_style',
        'fuel_type',
        'is_featured',
        'generate_report',
    )

    list_display_links = ('id', 'thumbnail', 'car_title')
    list_editable = ('is_featured',)

    search_fields = ('id', 'car_title', 'city', 'model', 'body_style', 'fuel_type')
    list_filter = ('city', 'model', 'body_style', 'fuel_type')


admin.site.register(Car, CarAdmin)
