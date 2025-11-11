from django.shortcuts import render


def profile_view(request):
    return render(request, 'users/Profile.html')

def login_view(request):
    return render(request, 'users/Login.html')

def register_view(request):
    return render(request, 'users/Register.html')
