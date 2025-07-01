from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from django.db.models import Count
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from .models import Profile
from django.utils import timezone
from .utils import send_verification_email
from social_django.models import UserSocialAuth

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user)
            messages.info(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('post_list')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

def verify_email(request, token):
    try:
        profile = get_object_or_404(Profile, verification_token=token)
        
        # Check if token is expired (7 days)
        if (timezone.now() - profile.token_created_at).days > 7:
            messages.error(request, 'The verification link has expired. Please request a new one.')
            return redirect('request_verification')
        
        if not profile.email_verified:
            profile.email_verified = True
            profile.save()
            messages.success(request, 'Your email has been verified successfully!')
        else:
            messages.info(request, 'Your email is already verified.')
        
        return redirect('profile')
    
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('home')

@login_required
def dashboard_view(request):
    # Get user's posts with annotation for comment count
    user_posts = Post.objects.filter(author=request.user).annotate(
        comment_count=Count('comments')
    ).order_by('-publish_date')[:5]
    
    # Get user's recent comments
    user_comments = Comment.objects.filter(email=request.user.email).order_by('-created_at')[:5]
    
    # Get post statistics
    post_stats = {
        'total_posts': Post.objects.filter(author=request.user).count(),
        'published_posts': Post.objects.filter(author=request.user, status='published').count(),
        'draft_posts': Post.objects.filter(author=request.user, status='draft').count(),
    }
    
    return render(request, 'accounts/dashboard.html', {
        'user_posts': user_posts,
        'user_comments': user_comments,
        'post_stats': post_stats,
    })

@login_required
def request_verification_email(request):
    if request.method == 'POST':
        if not request.user.profile.email_verified:
            new_token = request.user.profile.generate_new_token()
            send_verification_email(request.user)
            messages.success(request, 'A new verification email has been sent to your email address.')
            return redirect('profile')
        else:
            messages.info(request, 'Your email is already verified.')
            return redirect('profile')
    
    return render(request, 'accounts/request_verification.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('post_list')

@login_required
def profile_view(request):
    social_accounts = UserSocialAuth.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {'form': form, 'social_accounts': social_accounts})