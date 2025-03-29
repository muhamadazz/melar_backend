from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Akun berhasil dibuat! Silakan login.")

            # Redirect dengan reverse untuk menghindari broken URL
            response = HttpResponseRedirect(reverse("signup"))
            response.set_cookie("signup_success", "true", max_age=3)

            # login(request, user)  # Opsional: auto login setelah signup
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})
