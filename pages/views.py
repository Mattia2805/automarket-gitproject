from django.shortcuts import render, redirect
from .models import Team
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars = Car.objects.order_by('-created_date')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'teams' : teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    teams = Team.objects.all()
    data = {
        'teams' : teams,
    }
    return render(request, 'pages/about.html', data)

def services(request):
    return render(request, 'pages/services.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Professional email template
        email_subject = f"New Contact Message from AutoMarket: {subject}"
        message_body = f"""
        You have received a new message from AutoMarket website.

        ----------------------------
        Sender Information:
        ----------------------------
        Name: {name}
        Email: {email}
        Phone: {phone}

        ----------------------------
        Message:
        ----------------------------
        {message}

        ----------------------------
        Please respond promptly to the sender.
        ----------------------------
        """

        try:
            admin_info = User.objects.filter(is_superuser=True).first()
            admin_email = admin_info.email if admin_info else "admin@example.com"

            send_mail(
                email_subject,
                message_body,
                "m.maugeri2828@gmail.com",  
                [admin_email],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for contacting us. We will get back to you shortly.')
        except Exception as e:
            messages.error(request, f"An error occurred while sending your message: {e}")

        return redirect('contact')  

    return render(request, 'pages/contact.html')