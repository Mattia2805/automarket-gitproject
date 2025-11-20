from django.shortcuts import render, get_object_or_404
from .models import Car
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# List cars with pagination
def cars(request):
    cars = Car.objects.order_by('-created_date')
    paginator = Paginator(cars, 4)  # 4 cars per page
    page = request.GET.get('page')

    try:
        paged_cars = paginator.page(page)
    except PageNotAnInteger:
        paged_cars = paginator.page(1)
    except EmptyPage:
        paged_cars = paginator.page(paginator.num_pages)

    data = {
        'cars': paged_cars,
    }
    return render(request, 'cars/cars.html', data)

# Single car detail view
def car_detail(request, id):
    single_car = get_object_or_404(Car, pk=id)

    data = {
        'single_car': single_car,
    }
    return render(request, 'cars/car_detail.html', data)
