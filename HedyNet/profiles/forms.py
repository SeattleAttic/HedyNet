import django.forms as forms

from profiles import models

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['profile_access', 'display_name', 'legal_name', 'legal_name_access',
            'about', 'about_access', 'preferred_contact_method', 'preferred_phone',
            'preferred_email', 'preferred_address']

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
    class Meta:
        model = models.UserPhone
        fields = ['label', 'access', 'phone', 'notes']

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = models.UserEmail
        fields = ['label', 'access', 'email', 'notes']

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = models.UserAddress
        fields = ['label', 'access', 'address', 'notes']
