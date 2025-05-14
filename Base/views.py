from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from Base.models import Contact

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        if len(name) < 2 or len(name) > 30:
            messages.error(request, 'Length of name should be between 2 and 30 characters.')
            return render(request, 'home.html')

        if len(email) < 5 or len(email) > 100:
            messages.error(request, 'Invalid email address.')
            return render(request, 'home.html')

        # Save to database
        contact_instance = Contact(name=name, email=email, content=message_content)
        contact_instance.save()
        messages.success(request, 'Thank you for contacting me! Your message has been saved.')

        # Send email notification
        if getattr(settings, 'SEND_NOTIFICATION_EMAIL', False):
            try:
                send_mail(
                    'New Contact Form Submission',
                    f"Name: {name}\nEmail: {email}\nMessage: {message_content}",
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                print('✅ Email sent successfully')
            except Exception as e:
                print(f"❌ Failed to send email: {e}")

        return redirect('home')

    return render(request, 'home.html')
