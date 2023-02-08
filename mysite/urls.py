from django.contrib import admin
from django.urls import include, path
from app.views import edit_profile, profile, add_class, follow





urlpatterns = [
    path('', include('app.urls')),
    path('app/', include('app.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),

    #path('friends/', friendslist, name='edit_profile_page'),
    path('<int:pk>/profile/edit/', edit_profile, name='edit_profile_page'),
    path('class/addclass/', add_class, name='add_class'),
    path('follow/', follow, name='follow'),
]
