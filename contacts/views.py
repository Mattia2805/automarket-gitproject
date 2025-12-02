from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.contrib.auth.models import User

def inquiry(request):
    """Persist a car inquiry and notify site administrators via email."""
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        car_title = request.POST.get('car_title')
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        customer_need = request.POST.get('customer_need')
        city = request.POST.get('city')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')

        # If user is authenticated, override user_id for security
        if request.user.is_authenticated:
            user_id = request.user.id
            if Contact.objects.filter(car_id=car_id, user_id=user_id).exists():
                messages.error(
                    request,
                    'You have already made an inquiry about this car. Please wait until we get back to you.'
                )
                return redirect('/cars/' + car_id)

        # Create contact inquiry object
        contact = Contact(
            car_id=car_id,
            car_title=car_title,
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            customer_need=customer_need,
            city=city,
            email=email,
            phone=phone,
            message=message_text
        )
        contact.save()

        # Prepare a professional email for admin
        admin_info = User.objects.filter(is_superuser=True).first()
        admin_email = admin_info.email if admin_info else None

        if admin_email:
            email_subject = f"New Car Inquiry for {car_title}"
            email_body = f"""
            You have received a new inquiry for your car listing:

            --------------------------------------
            Car: {car_title} (ID: {car_id})
            --------------------------------------

            Customer Information:
            Name: {first_name} {last_name}
            Email: {email}
            Phone: {phone}
            City: {city}
            Need: {customer_need}

            Message:
            {message_text}

            --------------------------------------
            Please log in to your admin panel to respond.
            --------------------------------------
            """

            send_mail(
                email_subject,
                email_body,
                "m.maugeri2828@gmail.com",
                [admin_email],
                fail_silently=False,
            )

        messages.success(request, 'Your request has been submitted, we will get back to you shortly.')
        return redirect('/cars/' + car_id)