from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from Base.models import Contact

def contact(request):
    if request.method == "POST":
        print('POST request received')

        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Basic form validation
        if not name or len(name) < 2 or len(name) > 30:
            messages.error(request, 'Length of name should be greater than 2 and less than 30 characters')
            return render(request, 'home.html')

        if not email or len(email) < 5 or len(email) > 100:
            messages.error(request, 'Invalid email address')
            return render(request, 'home.html')

        if not message or len(message.strip()) == 0:
            messages.error(request, 'Message cannot be empty')
            return render(request, 'home.html')

        # Save to the database
        contact_instance = Contact(name=name, email=email, message=message)
        contact_instance.save()
        messages.success(request, 'Thank you for contacting me! Your message has been saved.')

        # Send email notification to yourself
        try:
            send_mail(
                'New Contact Form Submission',
                f"Name: {name}\nEmail: {email}\nMessage: {message}",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print('Email sent successfully')
        except Exception as e:
            print(f'Error sending email: {e}')

        return redirect('home')  # Redirect to home after successful submission

    return render(request, 'home.html')
