import unittest

from django.test import TestCase
from django.contrib.auth.models import User

from profiles.access import access_levels, can_access
from profiles.models import UserProfile
from profiles import constants

class AccessTestCase(TestCase):
    """
    A base class to use that sets up different users and profiles for
    the test case.
    """

    def setUp(self):
        """
        This is the function that sets up the following users/profiles:
        
        * member1
        * member2
        * admin1
        * admin2
        * registered
        """
        
        self.member1 = User.objects.create(username="member1")
        self.member1.save()
        self.member1_profile = UserProfile.objects.create(
            user = self.member1, status = constants.ACTIVE_STATUS) 
        self.member1_profile.save()

        self.member2 = User.objects.create(username="member2")
        self.member2.save()
        self.member2_profile = UserProfile.objects.create(
            user = self.member2, status = constants.ACTIVE_STATUS)
        self.member2_profile.save()

        self.admin1 = User.objects.create(username="admin1", is_staff = True)
        self.admin1.save()
        self.admin1_profile = UserProfile.objects.create(
            user = self.admin1, status = constants.ACTIVE_STATUS)
        self.admin1_profile.save()

        self.admin2 = User.objects.create(username="admin2", is_staff = True)
        self.admin2.save()
        self.admin2_profile = UserProfile.objects.create(
            user = self.admin2, status = constants.ACTIVE_STATUS)
        self.admin2_profile.save()

        self.registered1 = User.objects.create(username="registered1")
        self.registered1.save()
        self.registered1_profile = UserProfile.objects.create(
            user = self.registered1, status = constants.APPLYING_STATUS)
        self.registered1_profile.save()    

        self.registered2 = User.objects.create(username="registered2")
        self.registered2.save()
        self.registered2_profile = UserProfile.objects.create(
            user = self.registered2, status = constants.APPLYING_STATUS)
        self.registered2_profile.save()   

class AccessLevelsTestCase(AccessTestCase):
    """
    Test the access_levels method in access.py.  Test different configurations
    of owner and viewer, and make sure the correct valid access levels are returned.
    """

    def test_member_and_member(self):
        """Test correct access levels with a member as owner and a member
        as a viewer."""
        expected_access_levels = (constants.MEMBERS_ACCESS,
            constants.REGISTERED_ACCESS, constants.PUBLIC_ACCESS)
        owner = self.member1_profile
        viewer = self.member2_profile
        self.assertItemsEqual(expected_access_levels, 
            access_levels(owner, viewer))
        
    def test_member_and_none(self):
        """Test correct access levels with a member as owner and an
        anonymous viewer."""
        expected_access_levels = (constants.PUBLIC_ACCESS,)
        owner = self.member1_profile
        viewer = None
        self.assertItemsEqual(expected_access_levels, 
            access_levels(owner, viewer))
        
    def test_member_and_self(self):
        """Test correct access levels with a member as the owner and viewer."""
        expected_access_levels = (constants.MEMBERS_ACCESS, 
            constants.REGISTERED_ACCESS, constants.PUBLIC_ACCESS,
            constants.PRIVATE_ACCESS)
        owner = self.member1_profile
        viewer = self.member1_profile
        self.assertItemsEqual(expected_access_levels, 
            access_levels(owner, viewer))
        
    def test_member_and_registered(self):
        """Test correct access levels with a member as the owner and a
        registered user (but not a member) as the viewer."""
        expected_access_levels = (constants.PUBLIC_ACCESS,
            constants.REGISTERED_ACCESS)
        owner = self.member1_profile
        viewer = self.registered1_profile
        self.assertItemsEqual(expected_access_levels, 
            access_levels(owner, viewer))

class CanAccessTestCase(AccessTestCase):
    """
    Test the can_access method in access.py.  Test different configurations
    of owner and viewer, and make sure the correct valid access levels are
    returned.
    """
    
    def test_public(self):
        """
        Any combination of owner/viewer at the public level should
        be True.
        """

        # test member/anonymous viewing
        self.assertTrue(can_access(self.member1_profile, None,
            constants.PUBLIC_ACCESS))
        # test member/registered viewing
        self.assertTrue(can_access(self.member1_profile, self.registered1_profile,
            constants.PUBLIC_ACCESS))
        # test member/member viewing
        self.assertTrue(can_access(self.member1_profile, self.member2_profile,
            constants.PUBLIC_ACCESS))
        # test self viewing
        self.assertTrue(can_access(self.member1_profile, self.member1_profile,
            constants.PUBLIC_ACCESS))
        # test admin/member viewing
        self.assertTrue(can_access(self.admin1_profile, self.member1_profile,
            constants.PUBLIC_ACCESS))
        # test member/admin viewing
        self.assertTrue(can_access(self.member1_profile, self.admin1_profile,
            constants.PUBLIC_ACCESS))
        # test admin/admin viewing
        self.assertTrue(can_access(self.admin1_profile, self.admin2_profile,
            constants.PUBLIC_ACCESS))
    
    def test_registered(self):
        """
        If the viewer is anonymous, this should return False.
        """

        # only false case
        # test member/anonymous viewing
        self.assertFalse(can_access(self.member1_profile, None,
            constants.REGISTERED_ACCESS))

        # test member/registered viewing
        self.assertTrue(can_access(self.member1_profile, self.registered1_profile,
            constants.REGISTERED_ACCESS))
        # test member/member viewing
        self.assertTrue(can_access(self.member1_profile, self.member2_profile,
            constants.REGISTERED_ACCESS))
        # test self viewing
        self.assertTrue(can_access(self.member1_profile, self.member1_profile,
            constants.REGISTERED_ACCESS))
        # test admin/member viewing
        self.assertTrue(can_access(self.admin1_profile, self.member1_profile,
            constants.REGISTERED_ACCESS))
        # test member/admin viewing
        self.assertTrue(can_access(self.member1_profile, self.admin1_profile,
            constants.REGISTERED_ACCESS))
        # test admin/admin viewing
        self.assertTrue(can_access(self.admin1_profile, self.admin2_profile,
            constants.REGISTERED_ACCESS))        

    def test_member(self):
        """
        If the viewer is a member, this should return True.
        """

        # test member/anonymous viewing
        self.assertFalse(can_access(self.member1_profile, None,
            constants.MEMBERS_ACCESS))
        # test member/registered viewing
        self.assertFalse(can_access(self.member1_profile, self.registered1_profile,
            constants.MEMBERS_ACCESS))

        # test member/member viewing
        self.assertTrue(can_access(self.member1_profile, self.member2_profile,
            constants.MEMBERS_ACCESS))
        # test self viewing
        self.assertTrue(can_access(self.member1_profile, self.member1_profile,
            constants.MEMBERS_ACCESS))
        # test admin/member viewing
        self.assertTrue(can_access(self.admin1_profile, self.member1_profile,
            constants.MEMBERS_ACCESS))
        # test member/admin viewing
        self.assertTrue(can_access(self.member1_profile, self.admin1_profile,
            constants.MEMBERS_ACCESS))
        # test admin/admin viewing
        self.assertTrue(can_access(self.admin1_profile, self.admin2_profile,
            constants.MEMBERS_ACCESS))  

    def test_admin(self):
        """
        If the viewer is an admin, this should return True.
        """

        # test member/anonymous viewing
        self.assertFalse(can_access(self.member1_profile, None,
            constants.ADMIN_ACCESS))
        # test member/registered viewing
        self.assertFalse(can_access(self.member1_profile, self.registered1_profile,
            constants.ADMIN_ACCESS))
        # test member/member viewing
        self.assertFalse(can_access(self.member1_profile, self.member2_profile,
            constants.ADMIN_ACCESS))
         # test admin/member viewing
        self.assertFalse(can_access(self.admin1_profile, self.member1_profile,
            constants.ADMIN_ACCESS))
        
        # test self viewing -- the one member level that is true because
        # you can view your own things
        self.assertTrue(can_access(self.member1_profile, self.member1_profile,
            constants.ADMIN_ACCESS))
        # test member/admin viewing
        self.assertTrue(can_access(self.member1_profile, self.admin1_profile,
            constants.ADMIN_ACCESS))
        # test admin/admin viewing
        self.assertTrue(can_access(self.admin1_profile, self.admin2_profile,
            constants.ADMIN_ACCESS))  

    def test_private(self):
        """
        Any combination of owner/viewer at the private level except when
        the owner/viewer is the same returns False.
        """
        
        # only true case
        # test self viewing
        self.assertTrue(can_access(self.member1_profile, self.member1_profile,
            constants.PRIVATE_ACCESS))

        # test member/anonymous viewing
        self.assertFalse(can_access(self.member1_profile, None,
            constants.PRIVATE_ACCESS))
        # test member/registered viewing
        self.assertFalse(can_access(self.member1_profile, self.registered1_profile,
            constants.PRIVATE_ACCESS))
        # test member/member viewing
        self.assertFalse(can_access(self.member1_profile, self.member2_profile,
            constants.PRIVATE_ACCESS))
        # test admin/member viewing
        self.assertFalse(can_access(self.admin1_profile, self.member1_profile,
            constants.PRIVATE_ACCESS))
        # test member/admin viewing
        self.assertFalse(can_access(self.member1_profile, self.admin1_profile,
            constants.PRIVATE_ACCESS))
        # test admin/admin viewing
        self.assertFalse(can_access(self.admin1_profile, self.admin2_profile,
            constants.PRIVATE_ACCESS))
