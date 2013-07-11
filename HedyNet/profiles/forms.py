import django.forms as forms

from profiles.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_access', 'display_name', 'legal_name', 'legal_name_access',
            'preferred_contact_method']
