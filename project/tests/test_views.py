import os
import random
import string
import uuid
from datetime import date, datetime, timedelta
from unittest.mock import patch

from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from funding.models import FundingBody, FundingSource
from institution.models import Institution
from project.forms import (ProjectCreationForm,
                           ProjectUserMembershipCreationForm,
                           RSEAllocationRequestCreationForm,
                           SystemAllocationRequestCreationForm)
from project.models import (Project, ProjectCategory, ProjectUserMembership,
                            SystemAllocationRequest)
from project.tests.test_models import (ProjectCategoryTests, ProjectTests,
                                       ProjectUserMembershipTests)
from project.views import (ProjectAddAttributionView,
                           ProjectAndAllocationCreateView, ProjectCreateView,
                           ProjectDetailView, ProjectListView,
                           ProjectUserMembershipFormView,
                           ProjectUserMembershipListView,
                           ProjectUserRequestMembershipListView,
                           RSEAllocationCreateView, SystemAllocationCreateView,
                           SystemAllocationRequestDetailView)
from system.models import System
from users.models import CustomUser


class ProjectViewTests(TestCase):

    fixtures = [
        'institution/fixtures/tests/institutions.json',
        'users/fixtures/tests/users.json',
        'project/fixtures/tests/categories.json',
        'project/fixtures/tests/projects.json',
        'project/fixtures/tests/memberships.json',
        'funding/fixtures/tests/attributions.json',
        'system/fixtures/tests/systems.json'
    ]

    def setUp(self):
        self.project_applicant = CustomUser.objects.get(email='norman.gordon@example.ac.uk')
        
        # Applicant from an institution that does not verify users
        # and doesn't permit RSE time requests
        self.inst2_applicant = CustomUser.objects.get(email='test.user@example2.ac.uk')

        self.project = Project.objects.get(code='scw0000')
        self.project_owner = self.project.tech_lead

        self.projectmembership = ProjectUserMembership.objects.get(id=2)
        self.project_member = self.projectmembership.user

        permission = Permission.objects.get(name='Can change project user membership')
        self.project_owner.user_permissions.add(permission)
        self.inst2_applicant.user_permissions.add(permission)
        self.project_member.user_permissions.add(permission)

    def _access_view_as_unauthorised_application_user(self, url, expected_redirect_url):
        """
        Ensure an unauthorised application user can not access a url.

        Args:
            url (str): Url to view.
            expected_redirect_url (str): Expected redirect url.
        """
        headers = {
            'Shib-Identity-Provider': 'invald-identity-provider',
            'REMOTE_USER': 'invalid-remote-user',
        }
        response = self.client.get(
            url,
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect_url)


class ProjectCreateViewTests(ProjectViewTests, TestCase):

    def test_view_as_authorised_application_user_without_project_add_permission(self):
        """
        Ensure the project create view is not accessible to an authorised application user,
        who does not have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.project_applicant.email,
        }
        response = self.client.get(
            reverse('create-project'),
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_view_as_authorised_application_user_with_project_add_permission(self):
        """
        Ensure the project create view is accessible to an authorised application user,
        who does have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_owner.profile.institution.identity_provider,
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('create-project'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), ProjectCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectCreateView))

    def test_view_as_authorised_with_project_add_without_user_approval(self):
        """
        Ensure the project create view is accessible to an authorised application user,
        who does have the required permissions and who is not required to be authorised
        and the user in in awaiting approval status
        """
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('create-project'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), ProjectCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectCreateView))

    def test_view_as_authorised_with_project_add_without_user_approval(self):
        """
        Ensure the project create view is accessible to an authorised application user,
        who does have the required permissions and who is not required to be authorised
        and the user in in awaiting approval status
        """
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('create-project'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), ProjectCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectCreateView))

    def test_view_without_user_approval_with_project_add_permission(self):
        """
        Ensure the project create view is accessible to a user who is not required
        to be authorised, who does have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('create-allocation', args=[self.project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), SystemAllocationRequestCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), SystemAllocationCreateView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project create view is not accessible to an unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('create-project'),
            '/en-gb/accounts/login/?next=/en-gb/projects/create/',
        )


class RSEAllocationCreateViewTests(ProjectViewTests, TestCase):
    def test_view_as_user_at_institution_without_rse_requests(self):
        """
        Ensure the RSE allocation create view is not accessible to an
        authorised application user at an institution that doesn't allow
        RSE time requests.
        """
        project = Project.objects.get(code='scw0001')
        headers = {
            'Shib-Identity-Provider': (self.inst2_applicant
                                       .profile.institution.identity_provider),
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('request-project-rse-time', args=[project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url,
                         reverse('project-application-detail',
                                 args=[project.id]))

    def test_view_as_project_owner(self):
        """
        Ensure the RSE allocation create view is accessible to an authorised
        application user, who does have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': (self.project_owner.profile
                                       .institution.identity_provider),
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('request-project-rse-time', args=[self.project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'),
                                   RSEAllocationRequestCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'),
                                   RSEAllocationCreateView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the RSE allocation request create view is not accessible to an
        unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('request-project-rse-time', args=[self.project.id]),
            '/en-gb/accounts/login/?next=/en-gb/projects/applications/{}/rse-time-application/'.format(self.project.id),
        )


class SystemAllocationCreateViewTests(ProjectViewTests, TestCase):

    def test_view_as_authorised_application_user_without_project_add_permission(self):
        """
        Ensure the allocation create view is not accessible to an authorised application user,
        who does not have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.project_applicant.email,
        }
        response = self.client.get(
            reverse('create-allocation', args=[self.project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_view_as_authorised_application_user_with_project_add_permission(self):
        """
        Ensure the project create view is accessible to an authorised application user,
        who does have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_owner.profile.institution.identity_provider,
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('create-allocation', args=[self.project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), SystemAllocationRequestCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), SystemAllocationCreateView))

    def test_view_without_user_approval_with_project_add_permission(self):
        """
        Ensure the project create view is accessible to a user who is not required to be authorised,
        who does have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('create-allocation', args=[self.project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), SystemAllocationRequestCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), SystemAllocationCreateView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project create view is not accessible to an unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('create-allocation', args=[self.project.id]),
            '/en-gb/accounts/login/?next=/en-gb/projects/{}/create-allocation/'.format(self.project.id)
        )


class ProjectAndAllocationCreateViewTests(ProjectViewTests, TestCase):

    def test_view_as_authorised_application_user_without_project_add_permission(self):
        """
        Ensure the project create view is not accessible to an authorised application user,
        who does not have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.project_applicant.email,
        }
        response = self.client.get(
            reverse('create-project-and-allocation'),
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_view_as_authorised_application_user_with_project_add_permission(self):
        """
        Ensure the project create view is accessible to an authorised application user,
        who does have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_owner.profile.institution.identity_provider,
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('create-project-and-allocation'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('project_form'), ProjectCreationForm))
        self.assertTrue(isinstance(response.context_data.get('allocation_form'), SystemAllocationRequestCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectAndAllocationCreateView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project create view is not accessible to an unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('create-project-and-allocation'),
            '/en-gb/accounts/login/?next=/en-gb/projects/create-project-and-allocation/',
        )


class ProjectDetailViewTests(ProjectViewTests, TestCase):

    def test_view_as_authorised_application_user_without_project_add_permission(self):
        """
        Ensure the project detail view is not accessible to an authorised application user,
        who does not have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.project_applicant.email,
        }
        response = self.client.get(
            reverse('project-application-detail', args=[1]),
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_view_as_authorised_application_user_with_project_add_permission(self):
        """
        Ensure the project detail view is accessible to an authorised application user,
        who does have the required permissions.
        """
        project = Project.objects.get(tech_lead=self.project_owner)
        headers = {
            'Shib-Identity-Provider': self.project_owner.profile.institution.identity_provider,
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('project-application-detail', args=[project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.get('project'), project)
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectDetailView))

    def test_view_without_user_approval_with_project_add_permission(self):
        """
        Ensure the project detail view is accessible to a user who is not required to be authorised,
        who does have the required permissions.
        """
        project = Project.objects.get(tech_lead=self.inst2_applicant)
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('project-application-detail', args=[project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data.get('project'), project)
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectDetailView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project detail view is not accessible to an unauthorised application user.
        """
        project = Project.objects.get(tech_lead=self.project_owner)
        self._access_view_as_unauthorised_application_user(
            reverse('project-application-detail', args=[project.id]),
            '/en-gb/accounts/login/?next=/en-gb/projects/applications/1/',
        )


class ProjectUserMembershipFormViewTests(ProjectViewTests, TestCase):

    def test_view_as_authorised_application_user(self):
        """
        Ensure the project user membership form view is accessible to an authorised application user.
        """
        headers = {
            'Shib-Identity-Provider': self.project_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.project_applicant.email,
        }
        response = self.client.get(
            reverse('project-membership-create'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), ProjectUserMembershipCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectUserMembershipFormView))

    def test_view_without_user_authorisation(self):
        """
        Ensure the project user membership form view is accessible to an authorised application user.
        """
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('project-membership-create'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('form'), ProjectUserMembershipCreationForm))
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectUserMembershipFormView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project user membership form view is not accessible to an unauthorised
        application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-membership-create'),
            '/en-gb/accounts/login/?next=/en-gb/projects/join/',
        )


class ProjectUserRequestMembershipListViewTests(ProjectViewTests, TestCase):

    def test_view_as_authorised_application_user_without_project_change_membership_permission(self):
        """
        Ensure the project user request membership list view is not accessible to an authorised
        application user, who does not have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.project_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.project_applicant.email,
        }
        response = self.client.get(
            reverse('project-user-membership-request-list'),
            **headers
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_view_without_user_approval_with_project_change_membership_permission(self):
        """
        Ensure the project user request membership list view is accessible to an authorised
        application user, who does not have the required permissions.
        """
        headers = {
            'Shib-Identity-Provider': self.inst2_applicant.profile.institution.identity_provider,
            'REMOTE_USER': self.inst2_applicant.email,
        }
        response = self.client.get(
            reverse('project-user-membership-request-list'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectUserRequestMembershipListView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project user request membership list view is not accessible to an unauthorised
        application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-user-membership-request-list'),
            '/en-gb/accounts/login/?next=/en-gb/projects/memberships/user-requests/',
        )


class ProjectUserMembershipListViewTests(ProjectViewTests, TestCase):

    def test_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the project user membership list view.
        """
        accounts = [
            {
                'user': self.project_applicant,
                'expected_status_code': 200,
            },
            {
                'user': self.project_owner,
                'expected_status_code': 200,
            },
            {
                'user': self.inst2_applicant,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            user = account.get('user')
            headers = {
                'Shib-Identity-Provider': user.profile.institution.identity_provider,
                'REMOTE_USER': user.email,
            }
            response = self.client.get(
                reverse('project-membership-list'),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))
            self.assertTrue(isinstance(response.context_data.get('view'), ProjectUserMembershipListView))

    def test_view_as_an_unauthorised_user(self):
        """
        Ensure unauthorised users can not access the project user membership list view.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-membership-list'),
            '/en-gb/accounts/login/?next=/en-gb/projects/memberships/'
        )


class ProjectUserRequestMembershipUpdateViewTests(ProjectViewTests, TestCase):

    def setUp(self):
        super().setUp()
        code = ''.join(random.sample(string.ascii_uppercase + string.digits, k=10))

    @patch('project.openldap.project_membership_api',spec=[
        'list_project_memberships', 'create_project_membership', 'delete_project_membership'])
    def post_status_change(self, user, status_in, status_set, project_membership_api_mock):
        ''' Sign in with email and post a status change from status_in
        to status_set
        '''
        # Set the starting status
        self.projectmembership.status = status_in
        self.projectmembership.save()
        self.projectmembership.refresh_from_db()

        # Sign in as the user
        headers = {
            'Shib-Identity-Provider': user.profile.institution.identity_provider,
            'REMOTE_USER': user.email,
        }
        self.client.get(reverse('login'), **headers)

        # Set up request data
        url = reverse('project-user-membership-update',kwargs={'pk': self.projectmembership.id})
        data = {
            'project_id': self.projectmembership.project.id,
            'request_id': self.projectmembership.id,
            'status': status_set
        }

        # Post the change
        self.client.post(url, data)
        self.client.get(reverse('logout'))

    def test_accept_invite(self):
        ''' Check that the user can accept or decline the invitation to join a
        project, but cannot revoke or suspend membership'''

        self.projectmembership.initiated_by_user = False
        self.projectmembership.save()

        cases = [
            [ProjectUserMembership.AWAITING_AUTHORISATION, ProjectUserMembership.AUTHORISED, True],
            [ProjectUserMembership.AWAITING_AUTHORISATION, ProjectUserMembership.DECLINED, True],
            [ProjectUserMembership.AUTHORISED, ProjectUserMembership.REVOKED, False],
            [ProjectUserMembership.AUTHORISED, ProjectUserMembership.SUSPENDED, False],
        ]
        for status_in, status_set, result in cases:
            self.post_status_change(self.projectmembership.user, status_in, status_set)
            self.projectmembership.refresh_from_db()
            assert (self.projectmembership.status == status_set) == result

    def test_change_invited_member_status(self):
        ''' Check that the tech lead cannot accept or decline the invite, but can
        revoke or suspend the membership once accepted'''

        self.projectmembership.initiated_by_user = False
        self.projectmembership.save()

        cases = [
            [ProjectUserMembership.AWAITING_AUTHORISATION, ProjectUserMembership.AUTHORISED, False],
            [ProjectUserMembership.AWAITING_AUTHORISATION, ProjectUserMembership.DECLINED, False],
            [ProjectUserMembership.AUTHORISED, ProjectUserMembership.REVOKED, True],
            [ProjectUserMembership.AUTHORISED, ProjectUserMembership.SUSPENDED, True],
        ]
        for status_in, status_set, result in cases:
            self.post_status_change(self.project_owner, status_in, status_set)
            self.projectmembership.refresh_from_db()
            assert (self.projectmembership.status == status_set) == result

    def test_change_member_request_status(self):
        ''' Check that only the tech lead can change the
        status of a membership initiated by the tech lead '''

        self.projectmembership.initiated_by_user = True
        self.projectmembership.save()

        cases = [
            [ProjectUserMembership.AWAITING_AUTHORISATION, ProjectUserMembership.AUTHORISED],
            [ProjectUserMembership.AWAITING_AUTHORISATION, ProjectUserMembership.DECLINED],
            [ProjectUserMembership.AUTHORISED, ProjectUserMembership.REVOKED],
            [ProjectUserMembership.AUTHORISED, ProjectUserMembership.SUSPENDED],
        ]
        for status_in, status_set in cases:
            self.post_status_change(self.project_member, status_in, status_set)
            self.projectmembership.refresh_from_db()
            assert self.projectmembership.status == status_in

            self.post_status_change(self.project_owner, status_in, status_set)
            self.projectmembership.refresh_from_db()
            assert self.projectmembership.status == status_set

    def test_view_as_authorised_application_user(self):
        """
        Ensure the project user membership list view is accessible to an unauthorised application
        user.
        """
        headers = {
            'Shib-Identity-Provider': self.project_owner.profile.institution.identity_provider,
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('project-membership-list'),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('view'), ProjectUserMembershipListView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project user membership list view is not accessible to an unauthorised
        application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-membership-list'),
            '/en-gb/accounts/login/?next=/en-gb/projects/memberships/',
        )


class ProjectAddAttributionViewTests(ProjectViewTests, TestCase):
    def test_view_as_authorised_application_user(self):
        """
        Ensure the project add attribution view is accessible to an authorised
        application user.
        """
        headers = {
            'Shib-Identity-Provider': (self.project_owner.profile
                                       .institution.identity_provider),
            'REMOTE_USER': self.project_owner.email,
        }
        response = self.client.get(
            reverse('project-add-attributions', args=[self.project.id]),
            **headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context_data.get('view'),
                                   ProjectAddAttributionView))

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project add attribution view is not accessible to an
        unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-add-attributions', args=[self.project.id]),
            '/en-gb/accounts/login/?next=/en-gb/projects/applications/{}/attributions/'.format(self.project.id),
        )

        
class ProjectDocumentViewTests(ProjectViewTests, TestCase):
    def setUp(self):
        self.test_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_file.txt'
        )
        self.project = Project.objects.get(code='scw0000')
        self.institution = self.project.tech_lead.profile.institution
        self.system_allocation_request = (
            SystemAllocationRequest(
                project_id=self.project.id,
                start_date=date(2018, 8, 17),
                end_date=date(2019, 9, 17),
                requirements_software="none",
                requirements_training="none",
                requirements_onboarding="none",
                allocation_cputime=87695464,
                allocation_memory=1,
                allocation_storage_home=200,
                allocation_storage_scratch=1,
                document=self.test_file,
            )
        )
        self.system_allocation_request.save()

    def test_view_as_logged_in_users(self):
        accounts = [
            {
                'user': self.project.tech_lead,
                'code': 200,
                'content-type': 'text/plain'
            },
            {
                'user': CustomUser.objects.get(
                    email='admin.user@example.ac.uk'
                ),
                'code': 200,
                'content-type': 'text/plain'
            },
            {
                'user': CustomUser.objects.get(
                    email='norman.gordon@example.ac.uk'
                ),
                'code': 302,
                'url': '/en-gb/projects/applications/'
            }
        ]

        for account in accounts:
            headers = {
                'Shib-Identity-Provider': self.institution.identity_provider,
                'REMOTE_USER': account['user'].email,
            }
            response = self.client.get(
                reverse('project-application-document',
                        args=[self.system_allocation_request.id]),
                **headers
            )
            if 'content-type' in account:
                self.assertEqual(response['content-type'],
                                 account['content-type'])
            if 'url' in account:
                self.assertEqual(response.url, account['url'])

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project document view is not accessible to an unauthorised
        application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-application-document',
                    args=[self.system_allocation_request.id]),
            '/en-gb/projects/applications/',
            )


class ProjectMembershipInviteViewTests(ProjectViewTests, TestCase):
    def test_view_as_authorised_application_user(self):
        """
        Ensure the project membership invite view is accessible to a authorised
        application users only.
        """
        accounts = [
            # User not member of the project should be rejected
            {
                'user': CustomUser.objects.get(
                    email='project.member@example.ac.uk'
                ),
                'expected_status_code': 302,
                'expected_url': reverse('project-application-detail',
                                        args=[self.project.id])
            },
            # Member but not tech lead of the project should be rejected
            {
                'user': CustomUser.objects.get(
                    email='norman.gordon@example.ac.uk'
                ),
                'expected_status_code': 302,
                'expected_url': reverse('project-application-detail',
                                        args=[self.project.id])
            },
            # Tech lead of the project should be accepted
            {
                'user': CustomUser.objects.get(
                    email='shibboleth.user@example.ac.uk'
                ),
                'expected_status_code': 200
            }
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': (account['user'].profile.institution
                                           .identity_provider),
                'REMOTE_USER': account['user'].email,
            }
            response = self.client.get(
                reverse('project-membership-invite', args=[self.project.id]),
                **headers
            )
            self.assertEqual(response.status_code,
                             account['expected_status_code'])
            if 'expected_url' in account:
                self.assertEqual(response.url, account['expected_url'])

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project user membership list view is not accessible to an
        unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-membership-invite', args=[self.project.id]),
            reverse('project-application-detail', args=[self.project.id]),
        )


class ProjectSupervisorApproveViewTests(ProjectViewTests, TestCase):
    def setUp(self):
        self.user = CustomUser.objects.get(email='norman.gordon@example.ac.uk')
        self.project = Project.objects.create(
            title='Temporary test project for {}'.format(self.user.email),
            description='Project description',
            legacy_hpcw_id='HPCW-12345',
            legacy_arcca_id='ARCCA-12345',
            code='scw1004',
            institution_reference='BW-12345',
            department='School of Chemistry',
            supervisor_name="Joe Bloggs",
            supervisor_position="RSE",
            supervisor_email="shibboleth.user@example.ac.uk",
            tech_lead=self.user,
        )

    def test_view_as_logged_in_user(self):
        """
        Ensure the project supervisor approval view is not accessible to
        logged in users who are not the supervisor.
        """
        accounts = [
            {
                'user': CustomUser.objects.get(
                    email='norman.gordon@example.ac.uk'
                ),
                'expected_status_code': 302,
                'expected_url': reverse('home')
            },
            {
                'user': CustomUser.objects.get(
                    email='shibboleth.user@example.ac.uk'
                ),
                'expected_status_code': 200
            }
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': (account['user'].profile.institution
                                           .identity_provider),
                'REMOTE_USER': account['user'].email,
            }
            response = self.client.get(
                reverse('project-supervisor-approval', args=[self.project.id]),
                **headers
            )
            self.assertEqual(response.status_code,
                             account['expected_status_code'])
            if 'expected_url' in account:
                self.assertEqual(response.url, account['expected_url'])

    def test_view_as_unauthorised_application_user(self):
        """
        Ensure the project supervisor approval view is not accessible to an
        unauthorised application user.
        """
        self._access_view_as_unauthorised_application_user(
            reverse('project-supervisor-approval', args=[self.project.id]),
            '/en-gb/',
        )
