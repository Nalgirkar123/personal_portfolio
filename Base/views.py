from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from Base import models
from Base.models import Contact 

def contact(request):
    if request.method == "POST":
        print('POST request received')

        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        content = request.POST.get('content')

        # Basic form validation
        if len(name) < 2 or len(name) > 30:
            messages.error(request, 'Length of name should be greater than 2 and less than 30 characters')
            return render(request, 'home.html')

        if len(email) < 5 or len(email) > 100:  # Adjusted to a more reasonable range for emails
            messages.error(request, 'Invalid email address')
            return render(request, 'home.html')

        if len(number) < 10 or len(number) > 13:
            messages.error(request, 'Invalid phone number. Please enter a valid number')
            return render(request, 'home.html')

        # Save to the database
        contact_instance = Contact(name=name, email=email, content=content, number=number)
        contact_instance.save()
        messages.success(request, 'Thank you for contacting me! Your message has been saved.')

        # Send email notification
        if settings.SEND_NOTIFICATION_EMAIL:  # To enable or disable email notifications
            send_mail(
                'New Contact Form Submission',
                f"Name: {name}\nEmail: {email}\nNumber: {number}\nMessage: {content}",
                settings.EMAIL_HOST_USER,  # From Email
                [settings.EMAIL_HOST_USER],  # To Email (you can add more recipients)
                fail_silently=False,
            )
            print('Email sent successfully')

        print('Data saved and email sent')
        return redirect('home')  # Redirect to avoid resubmission on page refresh

    return render(request, 'home.html')
