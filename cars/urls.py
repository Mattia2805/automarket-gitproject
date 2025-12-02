from django.urls import path
from . import views

urlpatterns = [
    path('', views.cars, name='cars'),
    path('<int:id>', views.car_detail, name='car_detail'),
    path('search', views.search, name='search'),
    path("car_report/<int:car_id>/", views.car_report_pdf, name="car_report_pdf"),
]