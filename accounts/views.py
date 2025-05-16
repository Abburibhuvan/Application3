from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import get_user_model

User = get_user_model()

def custom_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        logout(request)  # Force logout before registration
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in with your credentials.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            try:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires when browser closes
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Exception as e:
                messages.error(request, 'An error occurred during login. Please try again.')
                print(f"Login error: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    try:
        user = request.user
        context = {
            'user': user,
            'role': user.get_role_display(),
            'full_name': user.get_full_name(),
        }
        return render(request, 'accounts/dashboard.html', context)
    except Exception as e:
        messages.error(request, 'An error occurred. Please try logging in again.')
        logout(request)
        return redirect('login') 