import django.forms as forms

from profiles import models

class UserProfileForm(forms.ModelForm):


    class Meta:
        model = models.UserProfile
        fields = ['profile_access', 'display_name', 'legal_name', 'legal_name_access',
            'public_about', 'about', 'about_access', 'preferred_contact_method',
            'preferred_phone', 'preferred_email', 'preferred_address',
            'dietary_considerations', 'emergency_contact']
        widgets = {
            'public_about': forms.Textarea(attrs={'rows':10}),
            'about': forms.Textarea(attrs={'rows':20}),
            'dietary_restrictions': forms.Textarea(attrs={'rows':4}),
            'emergency_contact': forms.Textarea(attrs={'rows':4}),
        }
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['preferred_phone'].queryset = models.UserPhone.objects.filter(
            profile = self.instance)
        self.fields['preferred_email'].queryset = models.UserEmail.objects.filter(
            profile = self.instance)
        self.fields['preferred_address'].queryset = models.UserAddress.objects.filter(
            profile = self.instance)
        
class MemberStatusChangeForm(forms.ModelForm):
    class Meta:
        model = models.MemberStatusChange
        fields = ['new_status', 'notes']

class UserPhoneForm(forms.ModelForm):
    
    preferred = forms.BooleanField(required = False)
    
    class Meta:
        model = models.UserPhone
        fields = ['label', 'access', 'phone', 'notes']

class UserEmailForm(forms.ModelForm):

    preferred = forms.BooleanField(required = False)

    class Meta:
        model = models.UserEmail
        fields = ['label', 'access', 'email', 'notes']

class UserAddressForm(forms.ModelForm):
    
    preferred = forms.BooleanField(required = False)

    class Meta:
        model = models.UserAddress
        fields = ['label', 'access', 'address', 'notes']

class UserExternalSiteForm(forms.ModelForm):
    class Meta:
        model = models.UserExternalSite
        fields = ['handle', 'link', 'site_category', 'custom_label', 'order',
            'access', 'notes']
