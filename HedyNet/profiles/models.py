from __future__ import unicode_literals

import datetime

from django.db import models
from django.db.models import Q

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from localflavor.us.models import PhoneNumberField

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from profiles import constants
from profiles import access

def filter_access_levels(query, field, access_levels, owner_field = None,
  owner_object = None):
    """Given a query, add an OR filter for the list of valid access levels
    applied to the given field. Can optionally add in an owner field and
    owner object that will be added, so that a user can see their own
    items regardless of """
    
    access_filter = reduce(
        lambda q,access_level: q|Q(**{field: access_level}), access_levels, Q())
    if owner_field and owner_object:
        access_filter = access_filter | Q(**{owner_field: owner_object})
    return query.filter(access_filter)

class UserProfile(models.Model):
    """Models the information we need for a user to be a member."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    status = models.CharField(max_length=20, choices=constants.STATUS_LEVELS, null=True)

    profile_access = models.CharField(max_length=20, choices=constants.BASIC_ACCESS_LEVELS, \
        default=constants.MEMBERS_ACCESS,
        help_text = """This determines who can see your profile.""")

    display_name = models.CharField(max_length=100, blank = True,
        help_text="Your display name throughout the site, which can be different from the default of your username.")

    legal_name = models.CharField(max_length=255, blank = True,
        help_text="Your legal name, which could be useful for administrative purposes.")
    legal_name_access = models.CharField(max_length=20, choices=constants.ACCESS_LEVELS, \
        default=constants.MEMBERS_ACCESS,
        help_text="Restrict who has access to your legal name.")

    public_about = models.TextField(blank = True,
        help_text="This about section will always be public.")
    about = models.TextField(blank = True, 
        help_text= "You can customize this area to tell others more about yourself." )
    about_access = models.CharField(max_length=20, choices=constants.BASIC_ACCESS_LEVELS,
        default=constants.MEMBERS_ACCESS,
        help_text="Restrict who has access to your about text.")

    dietary_considerations = models.TextField(blank = True,
        help_text="Do you have any dietary restrictions people should be aware of?")
    dietary_access = models.CharField(max_length=20, choices=constants.ACCESS_LEVELS,
        default=constants.MEMBERS_ACCESS,
        help_text="Restrict who has access to your dietary considerations.")

    preferred_contact_method = models.CharField(max_length=20,
        choices=constants.CONTACT_METHODS, default=constants.EMAIL_CONTACT,
        help_text="This lists your preferred contact method, so people know the best way to get in touch with you.")
    preferred_phone = models.ForeignKey('UserPhone', blank = True, null = True,
        help_text="This sets your preferred phone number, so if you have more than one you can say which one to use.",
        on_delete=models.SET_NULL)
    preferred_email = models.ForeignKey('UserEmail', blank = True, null = True,
        help_text="This sets your preferred email, so if you have more than one you can say which one to use.",
        on_delete=models.SET_NULL)
    preferred_address = models.ForeignKey('UserAddress', blank = True, null = True,
        help_text="This sets your preferred address, so if you have more than one you can say which one to use.",
        on_delete=models.SET_NULL)

    emergency_contact = models.TextField(blank = True, default="",
        help_text="Please describe who to contact in an emergency and how to best reach them. This is members only information.")

    became_member_on = models.DateField(null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)

    # TODO: add
    # avatar
    # portrait
    # using an access based media system

    def __unicode__(self):
        if self.display_name:
            return self.display_name
        else:
            return self.user.username

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.user.username})

    # TODO: override save function or add a listener; ensure that status changes
    # add a member status changes.  this can be on on creation of new profile
    # or modification of old one.
    # also need to make sure that became_member_on is set to an
    # appropriate value or delete it entirely and rely only on status changes

    def _is_member(self):
        return self.status == constants.ACTIVE_STATUS
    is_member = property(_is_member)
    
    def _is_admin(self):
        return self.user.is_staff
    is_admin = property(_is_admin)    
    
    def _latest_status(self):
        try:
            return MemberStatusChange.objects.filter().order_by('-changed_on')[0]
        except IndexError:
            return None
    latest_status = property(_latest_status)
    
    @staticmethod
    def get_profile(user):
        if not user or not user.is_authenticated():
            return None
        try:
            return UserProfile.objects.get(user = user)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_directory(viewer_profile = None, status = None):
        """Returns a list of profiles in the directory.  Giving a viewer_profile
        allows the viewer to see profiles that they have access to.  Giving
        a status filters the list to that type of membership status."""
        
        # we don't have any particular owner here, so get general access levels
        # for the viewer
        valid_access_levels = access.access_levels(None, viewer_profile)
        
        # okay, so if we're making a list of profiles we can show in this directory
        # view, we want items both in the valid access levels and in the
        # BASIC_ACCESS_LEVELS set that profile_access can be in
        # see this for more information on set operations:
        # http://docs.python.org/2/library/sets.html
        directory_access_levels = valid_access_levels.intersection(
            set([access_level[0] for access_level in 
            constants.BASIC_ACCESS_LEVELS]))
        
        # optionally filter by status; exclude status by prefixing with "-"
        if status:
            if status.startswith("-"):
                query = UserProfile.objects.exclude(status = status[1:])
            else:
                query = UserProfile.objects.filter(status = status)
            
        return filter_access_levels(query, "profile_access", directory_access_levels)
        
    def access_strip(self, access_levels = (constants.PUBLIC_ACCESS,),
        viewer_profile = None):
        """Strip away information from the model that does not have the given
        valid access levels."""
        
        # if the viewer is the owner of the profile, they can observe all the
        # current fields of data
        if viewer_profile == self:
            return
        
        if not self.legal_name_access in access_levels:
            self.legal_name = ""
        
        if not self.about_access in access_levels:
            self.about = ""
        
        if not constants.MEMBERS_ACCESS in access_levels:
            self.became_member_on = None
            self.emergency_contact = None

    def get_preferred_phone(self, access_levels = (constants.PUBLIC_ACCESS,), 
      viewer_profile = None):
        
        if self.preferred_phone and \
          self.preferred_phone.access in access_levels:
            return self.preferred_phone
            
        return None
        
    def get_preferred_email(self, access_levels = (constants.PUBLIC_ACCESS,),
      viewer_profile = None):
        
        if self.preferred_email and \
          self.preferred_email.access in access_levels:
            return self.preferred_email
            
        return None
        
    def get_preferred_address(self, access_levels = (constants.PUBLIC_ACCESS,),
      viewer_profile = None):
        
        if self.preferred_address and \
          self.preferred_address.access in access_levels:
            return self.preferred_address
            
        return None
        
    def get_phone_contacts(self, access_levels = (constants.PUBLIC_ACCESS,),
      viewer_profile = None):
        """Fetch a list of phone contacts, given an access level.  The default
        access level is public."""
        
        query = UserPhone.objects.filter(profile = self)
        return filter_access_levels(query, "access", access_levels, "profile",
            viewer_profile)
    
    def get_address_contacts(self, access_levels = (constants.PUBLIC_ACCESS,),
      viewer_profile = None):
        """Fetch a list of address contacts, given an access level.  The default
        access level is public."""
        
        query = UserAddress.objects.filter(profile = self)
        return filter_access_levels(query, "access", access_levels, "profile",
            viewer_profile)
        
    def get_email_contacts(self, access_levels = (constants.PUBLIC_ACCESS,),
      viewer_profile = None):
        """Fetch a list of email contacts, given an access level.  The default
        access level is public."""
        
        query = UserEmail.objects.filter(profile = self)
        return filter_access_levels(query, "access", access_levels, "profile",
            viewer_profile)

    def get_external_sites(self, access_levels = (constants.PUBLIC_ACCESS,),
        viewer_profile = None):
        """Fetch a list of external sites, given an access level.  The default
        access level is public."""
        
        query = UserExternalSite.objects.filter(profile = self)
        return filter_access_levels(query, "access", access_levels, "profile",
            viewer_profile).order_by('order')

class MemberStatusChange(models.Model):
    """A history of user status changes."""

    profile = models.ForeignKey('UserProfile')
    changed_on = models.DateTimeField(auto_now_add=True)
    # old status can be blank because a profile could previously not exist
    old_status = models.CharField(max_length=20, choices=constants.STATUS_LEVELS, \
        blank = True, null = True)
    new_status = models.CharField(max_length=20, choices=constants.STATUS_LEVELS)
    notes = models.TextField(blank=True, default="")

    class Meta:
        ordering = ['-changed_on']

    def save(self, *args, **kwargs):
        super(MemberStatusChange, self).save(*args, **kwargs)
        self.profile.status = self.new_status

        if self.new_status == constants.ACTIVE_STATUS and \
         not self.profile.became_member_on:
            self.profile.became_member_on = datetime.date.today()

        self.profile.save()

    def get_absolute_url(self):
        return reverse('member_status_change_detail', kwargs = {'username': self.profile.user.username, 'pk': self.pk})

class UserExternalSite(models.Model):

    profile = models.ForeignKey('UserProfile')

    handle = models.CharField(max_length=50, blank = True)
    link = models.URLField(blank = True)

    site_category = models.ForeignKey('othersites.SiteInfo', blank = True, null = True)
    custom_label = models.CharField(max_length=50, blank=True)

    order = models.PositiveIntegerField(default=100)
    access = models.CharField(max_length=20, choices=constants.ACCESS_LEVELS, \
        default = constants.MEMBERS_ACCESS)
    notes = models.TextField(blank = True, default="")

    def _get_label(self):
        if self.site_category and self.custom_label:
            return "%s (%s)" % (self.site_category.name, self.custom_label)
        elif self.site_category:
            return self.site_category.name
        elif self.custom_label:
            return self.custom_label
        return ""
    label = property(_get_label)

    class Meta:
        ordering = ['profile', '-order']
        index_together = [('profile', 'order')]

    def __unicode__(self):
        if self.site_category:
            return "%s (%s)" % (self.site_category, self.profile)
        if self.custom_label:
            return "%s (%s)" % (self.custom_label, self.profile)
        return "(No label) (%s)" % self.profile

class UserContactInfo(models.Model):

    profile = models.ForeignKey('UserProfile')
    label = models.CharField(max_length=30, blank = True)
    access = models.CharField(max_length=20, choices=constants.ACCESS_LEVELS, \
        default=constants.MEMBERS_ACCESS)
    notes = models.TextField(blank = True, default="")

    class Meta:
        abstract = True

class UserPhone(UserContactInfo):

    phone = PhoneNumberField()

    def __unicode__(self):
        return self.phone
        
    def get_absolute_url(self):
        return reverse('user_profile_phone_detail', 
            kwargs = {'username': self.profile.user.username, 'pk': self.pk})

    def _is_preferred(self):
        if self.profile.preferred_phone_id == self.id:
            return True
        return False
    is_preferred = property(_is_preferred)

    class Meta:
        unique_together = (('profile', 'phone'),)

class UserEmail(UserContactInfo):

    email = models.EmailField()

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user_profile_email_detail', 
            kwargs = {'username': self.profile.user.username, 'pk': self.pk})

    def _is_preferred(self):
        if self.profile.preferred_email_id == self.id:
            return True
        return False
    is_preferred = property(_is_preferred)

    class Meta:
        unique_together = (("profile", "email"),)

class UserAddress(UserContactInfo):

    address = models.TextField()

    def __unicode__(self):
        if self.label:
            return self.label
        return "address"
        
    def get_absolute_url(self):
        return reverse('user_profile_address_detail', 
            kwargs = {'username': self.profile.user.username, 'pk': self.pk})
    
    def _is_preferred(self):
        if self.profile.preferred_address_id == self.id:
            return True
        return False
    is_preferred = property(_is_preferred)
