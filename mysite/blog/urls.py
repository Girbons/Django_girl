from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from .import views
from django.contrib.auth.decorators import login_required
from .views import Registration, RegistrationComplete, Profile

urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', login_required(views.PostEdit.as_view()), name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', login_required(views.PostDelete.as_view()), name='post_delete'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', login_required(views.PostNew.as_view()), name='post_new'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'accounts/logout.html'},
        name='logout'),
    url('^accounts/register/$', Registration.as_view(), {'template_name': 'accounts/register.html'},
         name='register'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/register/registration_complete', RegistrationComplete.as_view(),
        name='registration_complete'),
    url('^accounts/profile', login_required(Profile.as_view()), name='profile'),
    url('^post/(?P<pk>[0-9]+)/comment/$', login_required(views.NewComment.as_view()),
        name='comment_new'),
    url('^post/(?P<post_pk>[0-9]+)/comment/(?P<pk>[0-9]+)/edit/$', login_required(views.CommentEdit.as_view()),
        name='comment_edit'),
    url('^post/(?P<post_pk>[0-9]+)/comment/(?P<pk>[0-9]+)/$', login_required(views.CommentDetail.as_view()),
        name='comment_detail'),
    url('^post/(?P<post_pk>[0-9]+)/comment/(?P<pk>[0-9]+)/delete/$', login_required(views.DeleteComment.as_view()),
        name='comment_delete'),
]
