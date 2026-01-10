from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages

class AccountAgeRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        if request.user.is_authenticated:
            account_age = timezone.now() - request.user.date_joined
            if account_age > timedelta(days=7):
                if not request.path.startswith("/accounts/logout/"):
                    messages.error(request, "انتهت صلاحية الحساب. تواصل مع الإدارة.")
                    return redirect("accounts:logout")

        response = self.get_response(request)
        return response
