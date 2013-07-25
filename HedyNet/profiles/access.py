from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User, AnonymousUser

from profiles import constants
from profiles import models
    
def access_levels(owner_userprofile, viewer_userprofile):
    """A shortcut function for efficiency in places like the profile,
    where it is useful to do the checks for all the access levels and
    return a dictionary, instead of manually checking each one.
    
    Accepts either UserProfile or User objects."""

    valid_access_levels = set([constants.PUBLIC_ACCESS])

    # Sometimes the viewer will be anonymous; should return 
    # ASAP in these instances
    if isinstance(viewer_userprofile, AnonymousUser):
        return valid_access_levels
        
    if isinstance(viewer_userprofile, User):
        viewer_userprofile = models.UserProfile.get_profile(viewer_userprofile)

    if isinstance(owner_userprofile, User):
        owner_userprofile = models.UserProfile.get_profile(owner_userprofile)

    # the only valid access value for non-logged in users is the above defined
    # public access level
    if not viewer_userprofile:
        logger.debug(valid_access_levels)
        return valid_access_levels
    
    # registered level add since viewer user profile exists
    valid_access_levels.add(constants.REGISTERED_ACCESS)
    
    # member access level added if viewer is a member
    if viewer_userprofile.is_member:
        valid_access_levels.add(constants.MEMBERS_ACCESS)
    
    # admin access level added if viewer is an admin
    if viewer_userprofile.is_admin:
        valid_access_levels.add(constants.ADMIN_ACCESS)
    
    # private access level added if owner is same as viewer
    if owner_userprofile and viewer_userprofile.pk == owner_userprofile.pk:
        valid_access_levels.add(constants.PRIVATE_ACCESS)
    
    logger.debug(valid_access_levels) 
    return valid_access_levels
    
def can_access(owner_userprofile, viewer_userprofile, access_level):
    """Given the profile of the owner of a given security level and the 
    access level set for the content, return True or False for whether or 
    not a give viewer can see it."""
    # public access--always true
    if access_level == constants.PUBLIC_ACCESS:
        return True
        
    # if it's not public and the user is not logged in (aka no profile)
    # no access
    if not viewer_userprofile:
        return False
        
    # we have a viewer profile, so someone is logged in; can return true
    # if our access level is registered level
    if access_level == constants.REGISTERED_ACCESS:
        return True
        
    # viewer and owner are the same, so can access
    # this also covers the case of constants.PRIVATE_ACCESS
    if owner_userprofile and owner_userprofile.pk == viewer_userprofile.pk:
        return True
        
    # members only access is met
    if viewer.is_member and access_level == constants.MEMBERS_ACCESS:
        return True
        
    # admin only access is met
    if view.is_admin and access_level == constants.ADMIN_ACCESS:
        return True
        
    # explicitly return False in all other cases
    # TODO: might want to log this, to see what situations aren't being caught
    # by the above
    return False
