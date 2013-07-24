from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from profiles import constants

def filter_access_levels(query, field, access_levels):
    """Given a query, add an OR filter for the list of valid access levels
    applied to the given field."""
    
    access_filter = reduce(
        lambda q,access_level: q|Q(**{field: access_level}), access_levels, Q())
    return query.filter(access_filter)

class UserProfile(models.Model):
    """Models the information we need for a user to be a member."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    status = models.CharField(max_length=20, choices=constants.STATUS_LEVELS, null=True)

    profile_access = models.CharField(max_length=20, choices=constants.BASIC_ACCESS_LEVELS, \
        default=constants.MEMBERS_ACCESS)

    display_name = models.CharField(max_length=50)

    legal_name = models.CharField(max_length=255, blank = True, null = True)
    legal_name_access = models.CharField(max_length=20, choices=constants.ACCESS_LEVELS, \
        default=constants.MEMBERS_ACCESS)

    #about = models.TextField(blank = True, help_text="You can use Markdown in this profile.")

    preferred_contact_method = models.CharField(max_length=20,
        choices=constants.CONTACT_METHODS, default=constants.EMAIL_CONTACT)
    preferred_phone = models.ForeignKey('UserPhone', blank = True, null = True)
    preferred_email = models.ForeignKey('UserEmail', blank = True, null = True)
    preferred_address = models.ForeignKey('UserAddress', blank = True, null = True)

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
    
    @staticmethod
    def get_profile(user):
        if not user or not user.is_authenticated():
            return None
        try:
            return UserProfile.objects.get(user = user)
        except ObjectDoesNotExist:
            return None
    
class MemberStatusChange(models.Model):
    """A history of user status changes."""

    profile = models.ForeignKey('UserProfile')
    changed_on = models.DateTimeField(auto_now_add=True)
    # old status can be blank because a profile could previously not exist
    old_status = models.CharField(max_length=20, choices=constants.STATUS_LEVELS, \
        blank = True, null = True)
    new_status = models.CharField(max_length=20, choices=constants.STATUS_LEVELS)
    notes = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        super(MemberStatusChange, self).save(*args, **kwargs)
        self.profile.status = self.new_status
        self.profile.save()

    def get_absolute_url(self):
        return reverse('member_status_change_detail', kwargs = {'username': self.profile.user.username, 'pk': self.pk})

class UserContactInfo(models.Model):

    profile = models.ForeignKey('UserProfile')
    label = models.CharField(max_length=30, blank = True)
    access = models.CharField(max_length=20, choices=constants.ACCESS_LEVELS, \
        default=constants.MEMBERS_ACCESS)
    notes = models.TextField(blank = True, default="")

    class Meta:
        abstract = True

class UserPhone(UserContactInfo):

    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone

    def get_absolute_url(self):
        return reverse('user_profile_phone_detail', kwargs = {'username': self.profile.user.username, 'pk': self.pk})

class UserEmail(UserContactInfo):

    email = models.EmailField()

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user_profile_email_detail', kwargs = {'username': self.profile.user.username, 'pk': self.pk})

class UserAddress(UserContactInfo):

    address = models.TextField()

    def __unicode__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('user_profile_address_detail', kwargs = {'username': self.profile.user.username, 'pk': self.pk})
