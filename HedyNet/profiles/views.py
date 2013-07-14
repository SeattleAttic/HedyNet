from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import User
from django.http import Http404
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

import profiles.models as models
from profiles import constants
from profiles.access import access_levels, can_access
from profiles import forms

def get_user_profile_or_404(username):

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
        
        # get the viewer and their valid access levels (in general)
        viewer_profile = models.UserProfile.get_profile(self.request.user)
        logger.debug("Viewing member directory by user: %s" % str(self.request.user))
        
        # we don't have any particular owner here, so get general access levels
        # for the viewer
        valid_access_levels = access_levels(None, viewer_profile)
        
        # okay, so if we're making a list of profiles we can show in this directory
        # view, we want items both in the valid access levels and in the
        # BASIC_ACCESS_LEVELS set that profile_access can be in
        # see this for more information on set operations:
        # http://docs.python.org/2/library/sets.html
        directory_access_levels = valid_access_levels.intersection(
            set([access_level[0] for access_level in 
            constants.BASIC_ACCESS_LEVELS]))

        logger.debug("Valid access levels for MemberDirectoryView: %s" % \
            str(directory_access_levels))
        # only show active members 
        query = models.UserProfile.objects.filter(status = constants.ACTIVE_STATUS)
        # create an OR filter for valid access levels 
        access_filter = reduce(
            lambda q,value: q|Q(profile_access=value), directory_access_levels, Q())  
        return query.filter(access_filter)

class UserProfileView(SingleObjectMixin):

    model = models.UserProfile
    
    def get_object(self, *args, **kwargs):
        """Modify the get_object to return a profile based on a username."""

        username = self.kwargs.get("username", None)

        return get_user_profile_or_404(username)

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        
        if self.request.user == self.object.user:
            context['can_edit'] = True
        else:
            context['can_edit'] = False

        return context

class UserProfileDetailView(UserProfileView, DetailView):
    context_object_name = "user_profile"

class UserProfileUpdateView(LoginRequiredMixin, UserProfileView, UpdateView):
    form_class = forms.UserProfileForm
    template_name_suffix = "_edit"
    context_object_name = "user_profile"

    #def get_context_data(self, *args, **kwargs):
    #    context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
    #    context['user_profile'] = 
    #    return context

    def get_object(self, *args, **kwargs):

        user_profile = super(UserProfileUpdateView, self).get_object(*args, **kwargs)

        if user_profile.user != self.request.user:
            raise PermissionDenied()
        else:
            return user_profile

class MemberStatusListView(LoginRequiredMixin, ListView):
    model = models.UserProfile
    template_name = "profiles/memberstatus_list.html"
    context_object_name = "user_profile_list"

class MemberStatusChangeDetailView(LoginRequiredMixin, DetailView):
    model = models.MemberStatusChange
    context_object_name = "member_status_change"

class MemberStatusChangeListView(LoginRequiredMixin, ListView):
    model = models.MemberStatusChange
    context_object_name = "member_status_change_list"

    def get_queryset(self, *args, **kwargs):

        username = self.kwargs.get("username", None)
        user_profile = get_user_profile_or_404(username)

        return models.MemberStatusChange.objects.filter(
            profile = user_profile).order_by('-changed_on')

    def get_context_data(self, *args, **kwargs):

        context = super(MemberStatusChangeListView, self).get_context_data(*args, **kwargs)

        username = self.kwargs.get("username", None)
        context["user_profile"] = get_user_profile_or_404(username)

        return context

class MemberStatusChangeCreateView(LoginRequiredMixin, CreateView):
    form_class = forms.MemberStatusChangeForm
    template_name = "profiles/memberstatuschange_add.html"

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
