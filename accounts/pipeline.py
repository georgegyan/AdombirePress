from .models import Profile

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.profile
        if not profile.profile_picture and 'picture' in response:
            profile.profile_picture = response['picture']['data']['url']
        profile.save()
    elif backend.name == 'google':
        profile = user.profile
        if not profile.profile_picture and response.get('picture'):
            profile.profile_picture = response['picture']
        profile.save()
    elif backend.name == 'github':
        profile = user.profile
        if not profile.profile_picture and response.get('avatar_url'):
            profile.profile_picture = response['avatar_url']
        profile.save()
    
    # Mark social-auth users as verified
    if not user.profile.email_verified:
        user.profile.email_verified = True
        user.profile.save()