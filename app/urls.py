from django.urls import path, include
from django.contrib import admin
from . import views
from django.views.generic import TemplateView
from .views import StudySessionDetailView,AddSessionView,DeleteSessionView,EnrolledSessionsView

urlpatterns = [
    path('', EnrolledSessionsView,name = "home"),
    path("", include("allauth.urls")),
    path('class/', views.get_class,name = "get_class"),
    path('search/', views.get_search,name = "search"),
    path('study_session_post/', AddSessionView,name = "post"),
    path('list/', views.post_list,name = 'list'),
    path('list/<int:pk>/', StudySessionDetailView.as_view(), name = "post_detail"),
    path('enroll/<int:pk>/', views.EnrollView, name = "enroll"),
    #path('',views.EnrolledSessionsView, name = "home"),
    path('list/edit/<int:pk>/', views.update_session, name = "edit_session"),
    path('list/<int:pk>/delete/', DeleteSessionView.as_view(), name = "delete_session"),
    path('my_post_session/',views.ListMyPostSessions, name = "my_post_session"),
    path('user_list/', views.user_list,name = 'userList'),
    path('userSearch/', views.get_user_search,name = "userSearch"),
    path('<int:pk>/profile/', views.profile, name='user_profile'),
    path('reply/<int:pk>', views.discussion, name="discuss"),
    path('friendlist/', views.friendspost, name="Friend"),
    path('unenroll/<int:pk>/', views.UnenrollView, name = "unEnroll"),

]
