from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    account_type = forms.ChoiceField(
        choices=[('reader', 'Reader'), ('author', 'Author')],
        widget=forms.RadioSelect,
        required=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'account_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Add to appropriate group
            account_type = self.cleaned_data['account_type']
            if account_type == 'author':
                author_group = Group.objects.get(name='Authors')
                user.groups.add(author_group)
            
            # Add default permissions
            user.user_permissions.add(
                Permission.objects.get(codename='add_comment'),
                Permission.objects.get(codename='view_post'),
            )
        
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'website', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
        }