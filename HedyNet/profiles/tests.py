import unittest

from django.test import TestCase
from django.contrib.auth.models import User

from profiles.access import access_levels
from profiles.models import UserProfile
from profiles import constants

class AccessLevelsTestCase(TestCase):

    def setUp(self):

        member1 = User.objects.create(username="member1")
        member1.save()
        member1_profile = UserProfile.objects.create(user = member1, status = constants.ACTIVE_STATUS) 
        member1_profile.save()

        member2 = User.objects.create(username="member2")
        member2.save()
        member2_profile = UserProfile.objects.create(user = member2, status = constants.ACTIVE_STATUS)
        member2_profile.save()

        admin1 = User.objects.create(username="admin1", is_staff = True)
        admin1.save()
        admin1_profile = UserProfile.objects.create(user = admin1, status = constants.ACTIVE_STATUS)
        admin1_profile.save()

        admin2 = User.objects.create(username="admin2")
        admin2.save()
        admin2_profile = UserProfile.objects.create(user = admin2, status = constants.ACTIVE_STATUS)
        admin2_profile.save()

        registered = User.objects.create(username="registered")
        registered.save()
        registered_profile = UserProfile.objects.create(user = registered, status = constants.APPLYING_STATUS)
        registered_profile.save()

        self.level_tests = [
           (member1_profile, member2_profile, (constants.MEMBERS_ACCESS, constants.REGISTERED_ACCESS, constants.PUBLIC_ACCESS)),
           (member1_profile, None, (constants.PUBLIC_ACCESS,)),
           (member1_profile, member1_profile, (constants.MEMBERS_ACCESS, constants.REGISTERED_ACCESS, constants.PUBLIC_ACCESS, constants.PRIVATE_ACCESS)),
           (member1_profile, registered_profile, (constants.PUBLIC_ACCESS, constants.REGISTERED_ACCESS)),
        ]
 
    def test_access_levels(self):
        """See that of the above definitions for function variables and expected results
           comes up true."""

        for owner, viewer, expected_access_levels in self.level_tests:
            # print "Viewer: %s, Owner: %s, Expected: %s" % (str(viewer), str(owner), str(expected_access_levels))
            self.assertItemsEqual(expected_access_levels, access_levels(owner, viewer))
