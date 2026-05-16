from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect, render

def home(request):
    return render(request, "main/index.html")

def about(request):
    return render(request, "about/index.html")

def contact(request):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not email or not subject or not message_text:
            error_message = "please fill in all fields."
            if is_ajax:
                return JsonResponse({"success": False, "message": error_message}, status=400)
            messages.error(request, error_message)
            return render(request, "contact/index.html")

        subject_full = f"[CEPAC Contact] {subject}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}"
        recipient_list = ["info@cepac-eg.com"]
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", email) or email

        try:
            email_message = EmailMessage(
                subject_full,
                message_body,
                from_email,
                recipient_list,
                reply_to=[email],
            )
            email_message.send(fail_silently=False)
            success_message = "Message sent successfully. Thank you for contacting us."
            if is_ajax:
                return JsonResponse({"success": True, "message": success_message})
            messages.success(request, success_message)
            return redirect("main:contact")
        except BadHeaderError:
            error_message = "There was an error with the email header. Please try again."
        except Exception:
            error_message = "An error occurred while sending the message. Please try again later."

        if is_ajax:
            return JsonResponse({"success": False, "message": error_message}, status=500)
        messages.error(request, error_message)

    return render(request, "contact/index.html")

def portfolio(request):
    return render(request, "portfolio/index.html")

def team(request):
    return render(request, "team/index.html")
def services(request):
    return render(request, "services/index.html")
