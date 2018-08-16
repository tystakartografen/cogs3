from . import views

from django.urls import path

urlpatterns = [
    path(
        'create/',
        views.ProjectCreateView.as_view(),
        name='create-project',
    ),
    path(
        'create-allocation/',
        views.SystemAllocationCreateView.as_view(),
        name='create-allocation',
    ),
    path(
        'create-project-and-allocation/',
        views.ProjectAndAllocationCreateView.as_view(),
        name='create-project-and-allocation',
    ),
    path(
        'rse-time/request/',
        views.RSEAllocationCreateView.as_view(),
        name='request-rse-time'
    ),
    path(
        'join/',
        views.ProjectUserMembershipFormView.as_view(),
        name='project-membership-create',
    ),
    path(
        'applications/',
        views.ProjectListView.as_view(),
        name='project-application-list',
    ),
    path(
        'rse-time/',
        views.ProjectListView.as_view(),
        name='rse-allocation-list',
    ),
    path(
        'applications/<int:pk>/',
        views.ProjectDetailView.as_view(),
        name='project-application-detail',
    ),
    path(
        'applications/<int:project>/rse-time-application/',
        views.RSEAllocationCreateView.as_view(),
        {'include_project': False},
        name='request-project-rse-time',
    ),
    path(
        'allocations/<int:pk>/',
        views.SystemAllocationRequestDetailView.as_view(),
        name='allocation-request-detail',
    ),
    path(
        'rse-time/<int:pk>/',
        views.RSEAllocationRequestDetailView.as_view(),
        name='rse-allocation-detail',
    ),
    path(
        'applications/<int:pk>/invite-user',
        views.ProjectMembesrshipInviteView.as_view(),
        name='project-membership-invite',
    ),
    path(
        'memberships/',
        views.ProjectUserMembershipListView.as_view(),
        name='project-membership-list',
    ),
    path(
        'memberships/update/<int:pk>/',
        views.ProjectUserRequestMembershipUpdateView.as_view(),
        name='project-user-membership-update',
    ),
    path(
        'memberships/user-requests/',
        views.ProjectUserRequestMembershipListView.as_view(),
        name='project-user-membership-request-list',
    ),
    path(
        'memberships/user-requests/update/<int:pk>/',
        views.ProjectUserRequestMembershipUpdateView.as_view(),
        name='project-user-membership-request-update',
    ),
    path(
        'applications/<int:pk>/document/',
        views.ProjectDocumentView.as_view(),
        name='project-application-document',
    ),
    path(
        'list_attributions/',
        views.list_attributions,
        name='list_attributions',
    ),
    path(
        'allocations/create',
        views.SystemAllocationCreateView.as_view(),
        name='create_application',
    ),
]
