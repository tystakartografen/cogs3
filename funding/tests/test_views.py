from django.test import TestCase
from django.urls import reverse

from funding.forms import FundingSourceForm
from funding.forms import PublicationForm
from funding.forms import AddFundingSourceForm
from funding.views import FundingSourceAddView
from funding.views import FundingSourceCreateView
from funding.views import PublicationCreateView
from funding.views import AttributionListView
from funding.views import AttributionUpdateView
from funding.views import AttributioneDeleteView
from users.models import CustomUser
from funding.models import FundingSource
from funding.models import Publication
from institution.models import Institution


class FundingViewTests(TestCase):

    fixtures = [
        'institution/fixtures/tests/institutions.json',
        'users/fixtures/tests/users.json',
        'funding/fixtures/tests/funding_bodies.json',
        'funding/fixtures/tests/attributions.json',
        'project/fixtures/tests/categories.json',
        'project/fixtures/tests/projects.json',
        'project/fixtures/tests/memberships.json',
    ]

    def access_view_as_unauthorised_user(self, path):
        """
        Ensure an unauthorised user can not access a particular view.

        Args:
            path (str): Path to view.
        """
        institution = Institution.objects.get(name="Example University")
        headers = {
            'Shib-Identity-Provider': institution.identity_provider,
            'REMOTE_USER': 'invalid-remote-user',
        }
        response = self.client.get(path, **headers)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('register'))


class FundingSourceCreateViewTests(FundingViewTests, TestCase):

    def test_fundingsource_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the funding source create view.
        """
        user = CustomUser.objects.get(email="shibboleth.user@example.ac.uk")
        user2 = CustomUser.objects.get(email="guest.user@external.ac.uk")
        user3 = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(name="Example University")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 200,
            },
            {
                'email': user2.email,
                'expected_status_code': 200,
            },
            {
                'email': user3.email,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse('create-funding-source'),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))
            self.assertTrue(isinstance(response.context_data.get('form'), FundingSourceForm))
            self.assertTrue(isinstance(response.context_data.get('view'), FundingSourceCreateView))

    def test_view_as_an_unauthorised_user(self):
        """
        Ensure unauthorised users can not access the project create view.
        """
        self.access_view_as_unauthorised_user(reverse('create-funding-source'))


class FundingSourceAddViewTests(FundingViewTests, TestCase):
    fixtures = [
        'institution/fixtures/tests/institutions.json',
        'users/fixtures/tests/users.json',
        'funding/fixtures/tests/funding_bodies.json',
        'funding/fixtures/tests/attributions.json',
    ]

    def test_add_fundingsource_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the funding source create view.
        """
        user = CustomUser.objects.get(email="shibboleth.user@example.ac.uk")
        user2 = CustomUser.objects.get(email="guest.user@external.ac.uk")
        institution = Institution.objects.get(name="Example University")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 200,
            },
            {
                'email': user2.email,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }

            # Test get. Response is a form
            response = self.client.get(
                reverse('add-funding-source'),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))
            self.assertTrue(isinstance(response.context_data.get('form'), AddFundingSourceForm))
            self.assertTrue(isinstance(response.context_data.get('view'), FundingSourceAddView))

            # Test post with new id. Redirects to create form
            response = self.client.post(
                reverse('add-funding-source'),
                data={
                    'identifier': 'n53c7',
                },
                **headers
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/en-gb/funding/create-funding-source/")

    def test_add_fundingsource_view_as_authorised_with_approval_required(self):
        """
        Ensure the correct account types can access the funding source create view.
        """
        user = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(base_domain="example2.ac.uk")
        accounts = [
            {
                'email': user.email,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }

            # Test get. Response is a form
            response = self.client.get(
                reverse('add-funding-source'),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))
            self.assertTrue(isinstance(response.context_data.get('form'), AddFundingSourceForm))
            self.assertTrue(isinstance(response.context_data.get('view'), FundingSourceAddView))

            # Test post with new id. Redirects to create form
            response = self.client.post(
                reverse('add-funding-source'),
                data={
                    'identifier': 'n53c7',
                },
                **headers
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/en-gb/funding/create-funding-source/")
            # Test post with existing id
            response = self.client.post(
                reverse('add-funding-source'),
                data={
                    'identifier': 'scw0001',
                },
                **headers
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, "/en-gb/funding/list/")

    def test_view_as_an_unauthorised_user(self):
        """
        Ensure unauthorised users can not access the project create view.
        """
        self.access_view_as_unauthorised_user(reverse('add-funding-source'))


class AttributionListViewTests(FundingViewTests, TestCase):

    def test_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the funding source list view.
        """
        user = CustomUser.objects.get(email="shibboleth.user@example.ac.uk")
        user2 = CustomUser.objects.get(email="guest.user@external.ac.uk")
        institution = Institution.objects.get(name="Example University")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 200,
            },
            {
                'email': user2.email,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse('list-attributions'),
                **headers
            )
            self.assertEqual(response.status_code,
                             account.get('expected_status_code'))
            self.assertTrue(isinstance(response.context_data.get('view'),
                                       AttributionListView))

    def test_view_as_an_unauthorised_user(self):
        """
        Ensure unauthorised users can not access the project create view.
        """
        self.access_view_as_unauthorised_user(reverse('list-attributions'))


class FundingSourceUpdateViewTests(FundingViewTests, TestCase):

    def test_fundingource_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the funding source list view.
        """
        user = CustomUser.objects.get(email="shibboleth.user@example.ac.uk")
        user2 = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(name="Example University")
        funding_source = FundingSource.objects.get(identifier="scw0001")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 200,
            },
            {
                'email': user2.email,
                'expected_status_code': 302,
            },
        ]
        for account in accounts:
            funding_source.pi_email = account.get('email')
            funding_source.save()
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse(
                    'update-attribution',
                    args=[funding_source.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code,
                             account.get('expected_status_code'))

            if response.status_code == 200:
                # Allowed to update
                self.assertTrue(isinstance(response.context_data.get('form'),
                                       FundingSourceForm))
                self.assertTrue(isinstance(response.context_data.get('view'),
                                       AttributionUpdateView))
                            
    def test_fundingource_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the funding source list view.
        """
        user = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(base_domain="example2.ac.uk")
        funding_source = FundingSource.objects.get(title="Test funding source 2")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 302,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse(
                    'update-attribution',
                    args=[funding_source.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code,
                             account.get('expected_status_code'))

    def test_publication_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the funding source list view.
        """
        user = CustomUser.objects.get(email="shibboleth.user@example.ac.uk")
        user2 = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(name="Example University")
        publication = Publication.objects.get(title="Test publication")

        accounts = [
            {
                'user': user,
                'expected_status_code': 200,
            },
            {
                'user': user2,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            publication.created_by = account.get('user')
            publication.save()
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('user').email,
            }
            response = self.client.get(
                reverse(
                    'update-attribution',
                    args=[publication.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code,
                             account.get('expected_status_code'))
            self.assertTrue(isinstance(response.context_data.get('form'),
                                       PublicationForm))
            self.assertTrue(isinstance(response.context_data.get('view'),
                                       AttributionUpdateView))

    def test_view_as_an_unauthorised_user(self):
        """
        Ensure unauthorised users can not access the project create view.
        """
        user = CustomUser.objects.get(email="guest.user@external.ac.uk")
        institution = Institution.objects.get(name="Example University")
        funding_source = FundingSource.objects.get(title="Test funding source")

        accounts = [
            {
                'user': user,
                'expected_status_code': 302,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('user').email,
            }
            response = self.client.get(
                reverse(
                    'update-attribution',
                    args=[funding_source.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))

        self.access_view_as_unauthorised_user(
            reverse(
                'update-attribution',
                args=[funding_source.id]
            )
        )


class FundingSourceDeleteViewTests(FundingViewTests, TestCase):

    def test_view_as_an_authorised_user(self):
        """
        Ensure the correct account types can access the delete view.
        """
        user = CustomUser.objects.get(email="shibboleth.user@example.ac.uk")
        institution = Institution.objects.get(name="Example University")
        funding_source = FundingSource.objects.get(title="Test funding source")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 200,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse(
                    'delete-attribution',
                    args=[funding_source.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))
            self.assertTrue(
                isinstance(
                    response.context_data.get('view'),
                    AttributioneDeleteView
                )
            )

    def test_view_as_an_unauthorised_user(self):
        """
        Ensure unauthorised users can not access the delete view.
        """
        user = CustomUser.objects.get(email="guest.user@external.ac.uk")
        user2 = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(name="Example University")
        funding_source = FundingSource.objects.get(title="Test funding source")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 302,
            },
            {
                'email': user2.email,
                'expected_status_code': 302,
            },
        ]
        for account in accounts:
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse(
                    'delete-attribution',
                    args=[funding_source.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))

        self.access_view_as_unauthorised_user(
            reverse(
                'delete-attribution',
                args=[funding_source.id]
            )
        )

    def test_view_without_user_approval(self):
        """
        Ensure unauthorised users can not access the delete view.
        """
        user = CustomUser.objects.get(email="test.user@example2.ac.uk")
        institution = Institution.objects.get(name="Example University")
        funding_source = FundingSource.objects.get(title="Test funding source")

        accounts = [
            {
                'email': user.email,
                'expected_status_code': 302,
            },
        ]
        for account in accounts:
            funding_source.pi_email = account.get('email')
            funding_source.save()
            headers = {
                'Shib-Identity-Provider': institution.identity_provider,
                'REMOTE_USER': account.get('email'),
            }
            response = self.client.get(
                reverse(
                    'delete-attribution',
                    args=[funding_source.id]
                ),
                **headers
            )
            self.assertEqual(response.status_code, account.get('expected_status_code'))

        self.access_view_as_unauthorised_user(
            reverse(
                'delete-attribution',
                args=[funding_source.id]
            )
        )