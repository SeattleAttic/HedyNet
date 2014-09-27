from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import User
from django.http import Http404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

import profiles.models as models
from profiles import constants
from profiles.access import access_levels, can_access
from profiles import forms

def get_user_profile_or_404(username):
    """This function tries to retrieve a user profile based off of the given
    user name or raises a 404 error."""

    try:
        user = User.objects.get(username = username)
    except ObjectDoesNotExist:
        raise Http404("No %(verbose_name)s found matching the username" %
            {'verbose_name': models.UserProfile._meta.verbose_name})
    try:
        user_profile, created = models.UserProfile.objects.get_or_create(user = user)
    except ObjectDoesNotExist:
        raise Http404("No %(verbose_name)s found matching the username" %
            {'verbose_name': models.UserProfile._meta.verbose_name})

    return user_profile

class MemberDirectoryView(ListView):
    context_object_name = "user_profile_list"
    model = models.UserProfile
    
    def get_queryset(self):
        
        # get the viewer's profile
        viewer_profile = models.UserProfile.get_profile(self.request.user)
                
        # are we filtering?
        profile_filter = self.request.GET.get('filter')
        
        if profile_filter == "nonmembers":
            return models.UserProfile.get_directory(viewer_profile,
                status = "-" + constants.ACTIVE_STATUS)
        else:
            return models.UserProfile.get_directory(viewer_profile,
                status = constants.ACTIVE_STATUS)

    def get_context_data(self, *args, **kwargs):
        context = super(MemberDirectoryView, self).get_context_data(**kwargs)

        # add the viewer's profile to this view
        self.viewer_profile = models.UserProfile.get_profile(self.request.user)

        valid_access_levels = access_levels(None, self.viewer_profile)

        # strip off all data that can't be seen by the current
        # viewer from each profile
        # this way template makers cannot expose data by accident
        [profile.access_strip(access_levels = valid_access_levels,
            viewer_profile = self.viewer_profile)
            for profile in context["user_profile_list"]]

        # are we filtering?
        profile_filter = self.request.GET.get('filter')
        
        if profile_filter == "nonmembers":
            context["filter"] = "nonmembers"
        else:
            context["filter"] = "members"

        return context

class UserProfileView(SingleObjectMixin):

    model = models.UserProfile
    
    def get_object(self, *args, **kwargs):
        """Modify the get_object to return a profile based on a username."""

        username = self.kwargs.get("username", None)
                
        user_profile = get_user_profile_or_404(username)

        # add valid access levels to this view
        self.valid_access_levels = access_levels(user_profile.user, self.request.user)
        # add the viewer's profile to this view
        self.viewer_profile = models.UserProfile.get_profile(self.request.user)

        if (not user_profile.profile_access in self.valid_access_levels) and \
          (not user_profile.user_id == self.request.user.id):
            raise Http404("No %(verbose_name)s found matching the username" %
                {'verbose_name': models.UserProfile._meta.verbose_name})

        # strip the profile to only contain information present
        # at the valid access level
        user_profile.access_strip(self.valid_access_levels, self.viewer_profile)
        
        return user_profile

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        
        if self.request.user == self.object.user:
            context['can_edit'] = True
        else:
            context['can_edit'] = False
        
        valid_access_levels = access_levels(self.object, self.viewer_profile)
        
        context['phone_contacts'] = self.object.get_phone_contacts(
            self.valid_access_levels, self.viewer_profile)
        context['address_contacts'] = self.object.get_address_contacts(
            self.valid_access_levels, self.viewer_profile)
        context['email_contacts'] = self.object.get_email_contacts(
            self.valid_access_levels, self.viewer_profile)
        context['external_sites'] = self.object.get_external_sites(
            self.valid_access_levels, self.viewer_profile)
        
        context['preferred_phone'] = self.object.get_preferred_phone(
            self.valid_access_levels, self.viewer_profile)
        context['preferred_email'] = self.object.get_preferred_email(
            self.valid_access_levels, self.viewer_profile)
        context['preferred_address'] = self.object.get_preferred_address(
            self.valid_access_levels, self.viewer_profile)
        
        return context

class UserProfileDetailView(UserProfileView, DetailView):
    context_object_name = "user_profile"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)

        # add the viewer's profile to this view
        self.viewer_profile = models.UserProfile.get_profile(self.request.user)
        valid_access_levels = access_levels(self.object, self.viewer_profile)
        self.object.access_strip(access_levels = valid_access_levels,
            viewer_profile = self.viewer_profile)

        return context
        
class UserProfileUpdateView(LoginRequiredMixin, UserProfileView, UpdateView):
    form_class = forms.UserProfileForm
    template_name_suffix = "_edit"
    context_object_name = "user_profile"

    def get_object(self, *args, **kwargs):

        user_profile = super(UserProfileUpdateView, self).get_object(*args, **kwargs)

        # only the owner of the profile can edit it
        if user_profile.user != self.request.user:
            raise PermissionDenied()
        else:
            return user_profile

class UserContactInfoView(LoginRequiredMixin):
    def get_context_data(self, *args, **kwargs):

        context = super(UserContactInfoView, self).get_context_data(*args, **kwargs)

        viewer_profile = models.UserProfile.get_profile(self.request.user)
        context["username"] = self.kwargs.get("username", None)
        context["user_profile"] = get_user_profile_or_404(context["username"])

        if self.object:
            owner_profile = self.object.profile
            # pass in can_edit flag if viewer of the profile is also the owner
            # it will then be used as a conditional to render edit buttons
            context["can_edit"] = owner_profile == viewer_profile
            
            # check access for both the profile and the contact
            valid_profile_access = can_access(owner_profile, viewer_profile, 
                owner_profile.profile_access)
            valid_contact_access = can_access(owner_profile, viewer_profile,
                self.object.access)
            
            # only let the page be viewed if there is valid access
            if not (valid_profile_access and valid_contact_access):
                raise PermissionDenied
        
        self.username = context["username"]
        self.profile = context["user_profile"]

        return context

class UserContactInfoEditView(UserContactInfoView):

    def dispatch(self, request, *args, **kwargs):
        self.username = self.kwargs.get("username", None)
        self.profile = get_user_profile_or_404(self.username)

        # only owner of the profile can edit a given contact view
        if self.request.user != self.profile.user:
            raise PermissionDenied

        return super(UserContactInfoView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):

        username = self.kwargs.get("username", None)

        if isinstance(self.object, models.UserExternalSite):
            return reverse("user_profile", kwargs={"username": username})

        return reverse("user_contact", kwargs={"username": username})

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # give this object a profile automatically
        self.object.profile = self.profile
        self.object.save()
        
        # if we've decided this is a preferred object, save that on the profile
        if 'preferred' in form.cleaned_data and form.cleaned_data['preferred']:
            field = ''
            if isinstance(self.object, models.UserPhone):
                field = 'preferred_phone'
            elif isinstance(self.object, models.UserEmail):
                field = 'preferred_email'
            elif isinstance(self.object, models.UserAddress):
                field = 'preferred_address'
            
            if field:
                setattr(self.profile, field, self.object)
                self.profile.save()

        return super(ModelFormMixin, self).form_valid(form)

    def get_form_kwargs(self, **kwargs):
        
        kwargs = super(UserContactInfoEditView, self).get_form_kwargs(**kwargs)

        if self.object and not isinstance(self.object, models.UserExternalSite):
            kwargs['initial'] = {'preferred': self.object.is_preferred}

        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(UserContactInfoEditView, self).get_context_data(**kwargs)

        if isinstance(self, CreateView):
            context["action"] = "add"
        if isinstance(self, UpdateView):
            context["action"] = "edit"

        return context
            
class UserPhoneCreateView(UserContactInfoEditView, CreateView):
    form_class = forms.UserPhoneForm
    template_name = "profiles/userphone_add.html"

class UserEmailCreateView(UserContactInfoEditView, CreateView):
    form_class = forms.UserEmailForm
    template_name = "profiles/useremail_add.html"

class UserAddressCreateView(UserContactInfoEditView, CreateView):
    form_class = forms.UserAddressForm
    template_name = "profiles/useraddress_add.html"

class UserExternalSiteCreateView(UserContactInfoEditView, CreateView):
    form_class = forms.UserExternalSiteForm
    template_name = "profiles/userexternalsite_add.html"

class UserPhoneUpdateView(UserContactInfoEditView, UpdateView):
    model = models.UserPhone    
    form_class = forms.UserPhoneForm
    template_name = "profiles/userphone_add.html"

class UserEmailUpdateView(UserContactInfoEditView, UpdateView):
    model = models.UserEmail
    form_class = forms.UserEmailForm
    template_name = "profiles/useremail_add.html"

class UserAddressUpdateView(UserContactInfoEditView, UpdateView):
    model = models.UserAddress
    form_class = forms.UserAddressForm
    template_name = "profiles/useraddress_add.html"

class UserExternalSiteUpdateView(UserContactInfoEditView, UpdateView):
    model = models.UserExternalSite
    form_class = forms.UserExternalSiteForm
    template_name = "profiles/userexternalsite_add.html"

class UserPhoneDetailView(UserContactInfoView, DetailView):
    model = models.UserPhone
    context_object_name = "user_phone"

class UserAddressDetailView(UserContactInfoView, DetailView):
    model = models.UserAddress
    context_object_name = "user_address"

class UserEmailDetailView(UserContactInfoView, DetailView):
    model = models.UserEmail
    context_object_name = "user_email"

class UserExternalSiteDetailView(UserContactInfoView, DetailView):
    model = models.UserExternalSite
    context_object_name = "user_externalsite"

class UserContactInfoDeleteView(LoginRequiredMixin, DeleteView):
    
    def get_success_url(self, *args, **kwargs):

        username = self.kwargs.get("username", None)

        if isinstance(self.object, models.UserExternalSite):
            return reverse("user_profile", kwargs={"username": username})

        return reverse("user_contact", kwargs={"username": username})

class UserPhoneDeleteView(UserContactInfoDeleteView):
    model = models.UserPhone
    context_object_name = "user_phone"

class UserAddressDeleteView(UserContactInfoDeleteView):
    model = models.UserAddress
    context_object_name = "user_address"

class UserEmailDeleteView(UserContactInfoDeleteView):
    model = models.UserEmail
    context_object_name = "user_email"

class UserExternalSiteDeleteView(UserContactInfoDeleteView):
    model = models.UserExternalSite
    context_object_name = "user_externalsite"

class MemberStatusListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.UserProfile
    template_name = "profiles/memberstatus_list.html"
    context_object_name = "user_profile_list"
    permission_required = "profiles.add_memberstatuschange"
    raise_exception = True

class MemberStatusChangeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.MemberStatusChange
    context_object_name = "member_status_change"
    permission_required = "profiles.add_memberstatuschange"
    raise_exception = True

class MemberStatusChangeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.MemberStatusChange
    context_object_name = "member_status_change_list"
    permission_required = "profiles.add_memberstatuschange"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.username = self.kwargs.get("username", None)
        self.user_profile = get_user_profile_or_404(self.username)
        self.viewer_profile = models.UserProfile.get_profile(self.request.user)

        return super(MemberStatusChangeListView, self).get(self, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):

        return models.MemberStatusChange.objects.filter(
            profile = self.user_profile).order_by('-changed_on')

    def get_context_data(self, *args, **kwargs):

        context = super(MemberStatusChangeListView, self).get_context_data(*args, **kwargs)

        context["user_profile"] = self.user_profile

        return context

class MemberStatusChangeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = forms.MemberStatusChangeForm
    template_name = "profiles/memberstatuschange_add.html"
    permission_required = "profiles.add_memberstatuschange"
    raise_exception = True

    def get_success_url(self, *args, **kwargs):

        return reverse("member_status_change_list", kwargs={"username": self.kwargs.get("username", None)})

    def get_context_data(self, *args, **kwargs):
        context = super(MemberStatusChangeCreateView, self).get_context_data(*args, **kwargs)

        username = self.kwargs.get("username", None)
        user_profile = get_user_profile_or_404(username)

        try:
            last_status_change = models.MemberStatusChange.objects.filter(
                profile = user_profile).order_by('-changed_on')[0]
        except:
            last_status_change = None

        context["user_profile"] = user_profile
        context["last_status_change"] = last_status_change

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        username = self.kwargs.get("username", None)
        self.object.profile = get_user_profile_or_404(username)
        self.object.old_status = self.object.profile.status
        self.object.save()

        return super(ModelFormMixin, self).form_valid(form)

class MemberOnlyPassView(UserPassesTestMixin, TemplateView):
    """
    A convenience view that will let a viewer see a page only if they are a member.
    """
    def test_func(self, user):

        if not user.id:
            return False

        try:
            user_profile, created = models.UserProfile.objects.get_or_create(user__id = user.id)
        except ObjectDoesNotExist:
            return False

        return user_profile.is_member
