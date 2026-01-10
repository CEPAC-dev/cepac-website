from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse
from .forms import LoginForm
from .forms import SignupForm, LoginForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح. مرحباً بك!")
            return redirect("accounts:login")
        else:
            messages.error(request, "هناك أخطاء في النموذج. راجع المدخلات.")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get("next") or "/"
            return redirect(next_url)
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
    
    return render(request, "accounts/login.html", {"form": form})




@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج.")
    return redirect("accounts:login")
