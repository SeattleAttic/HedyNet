from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

import profiles.models as models
from profiles import constants
from profiles.access import access_levels, can_access

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

class UserProfileDetailView(DetailView):
    model = models.UserProfile
    context_object_name = "user_profile"

    def get_object(self):
        """Modify the get_object to return a profile based on a username."""

        try:
            username = self.kwargs.get("username", None)
            profile = models.UserProfile.objects.get(user__username = username)
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name}) 

        return profile   
 
# TODO: User Profile editing view for users editing their own profile
# TODO: User Profile editing view for admins editing the status of somebody else
